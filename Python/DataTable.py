import pandas as pd
import numpy as np
from camelot import read_pdf, plot
from docx import Document, table
import os
import errno


MEASURES_HEADERS = ["#", "Recovery measures"]
INDEX_HEADER = "#"
JOIN_HEADER = "Recovery measures"


class TableDoc:
    """ Either a Resdoc, recovery plan or action plan document containing
    tabular data to parse and save.
    """

    def __init__(self, doc_file_path):
        self.metadata_dict = {}
        self.doc_path = doc_file_path
        self.dt_list = []  # doc table list
        self.measures_list = []
        self.out_dt = None

        # headers:
        self.header_dict = {"measures_headers": [],
                            "index_header": "",
                            "join_header": ""
                            }

        # make sure the filepath exists and is either a pdf or a Word doc:
        if not os.path.isfile(self.doc_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), doc_file_path)
        elif not self.doc_path.endswith((".doc", ".docx", ".pdf")):
            raise Exception("File type not supported, must be PDF or Word document.")

        self.scrape_doc()
        self.join_data()
        self.add_metadata()

    def scrape_doc(self):
        # checks if doc is word or pdf and scrapes it accordingly
        if self.doc_path.endswith((".doc", ".docx")):
            self.scrape_word()
        elif self.doc_path.endswith(".pdf"):
            self.scrape_pdf()
        else:
            raise Exception("File type not supported, must be PDF or Word document.")

    def scrape_pdf(self, line_scale=50):
        # very not supported yet....
        self.dt_list = read_pdf(self.doc_path, pages="all", line_scale=line_scale)

    def scrape_word(self):
        # function that extracts all the tables from a Word doc and saves them to self.dt_list as DocTable objects
        recovery_docx = Document(self.doc_path)
        self.dt_list = [DocTable(raw_table, self.header_dict) for raw_table in recovery_docx.tables]
        self.dt_list = [dt for dt in self.dt_list if dt.is_valid]
        self.measures_list = [dt for dt in self.dt_list if dt.is_measures_table]

    def add_metadata(self):
        # Append metadata values to the output dt:
        self.out_dt.add_metadata(self.metadata_dict)

    def join_data(self):
        # loops through self.measures_list and converts all the tables into a single output, ready for writing into an
        # excel/etc.
        if len(self.measures_list):
            self.out_dt = self.measures_list[0]
            for measure_dt in self.measures_list[1:]:
                self.out_dt.merge_tables(measure_dt.df)

    def write_to_excel(self, outpath):
        # Writes the output df into an excel sheet and opens the sheet
        self.out_dt.df.to_excel(outpath, index=False)
        os.startfile(outpath)

    def show_grid_lines(self, table_index):
        # for pdfs
        # shows the grid lines for camelot tables, useful for debugging
        return plot(self.df_list[table_index], kind='grid').show()

    def parser_report(self, table_index):
        # for pdfs
        # shows the report for a camelot table, may be useful for QC
        return self.df_list[table_index].parsing_report


class DocTable:
    """ An individual table as extracted from the document in DocTable
    Each table extracted from the word or PDF files is called a DocTable
    DocTable is used in class TableDoc
    """

    def __init__(self, raw_table, header_dict):
        self.df = pd.DataFrame()

        self.measures_headers = header_dict["measures_headers"]
        self.index_header = header_dict["index_header"]
        self.join_header = header_dict["join_header"]

        self.is_valid = False  # is this a valid table with data?
        self.is_measures_table = False  # does this table contain recovery measures?

        # upon init, the input datatable should get cleaned, classified and stored as a class attribute
        if raw_table is not None and type(raw_table) == table.Table:
            self.df = docx_table_to_pd(raw_table)
            self.clean()
            self.set_headers()
            self.set_table_type()
            self.is_valid = True

    def clean(self):
        # The input table should be converted into a pd dataframe, with various checks to set flags
        # remove regex values
        self.df = self.df.replace(r'\r+|\n+|\t+', '', regex=True)
        self.df = self.df.replace('', np.nan)

    def set_headers(self):
        # set the first row as the column headers, code from:
        # https://stackoverflow.com/questions/31328861/python-pandas-replacing-header-with-top-row
        new_header = self.df.iloc[0]
        self.df = self.df[1:]
        self.df.columns = new_header

    def set_table_type(self):
        # sets the flag and drops any uneeded columns
        if all([header in self.df.columns for header in self.measures_headers]):
            self.is_measures_table = True
            self.df = self.df[self.measures_headers]


    def merge_tables(self, df_to_merge):
        # Merge this table with another valid DocTable
        # look into this to merge rows split over pages:
        # https://stackoverflow.com/questions/40733386/python-pandas-merge-rows-if-some-values-are-blank
        self.df = pd.concat([self.df, df_to_merge], axis=0)
        # forward fill in any empty index column values:
        self.df.loc[:, self.index_header] = self.df.loc[:, self.index_header].ffill()
        self.df = self.df.groupby([self.index_header], as_index=False, sort=False)[self.join_header].apply(lambda x: ' '.join(x.astype(str)))

    def add_metadata(self, metadata_values):
        # given some metadata, add those columns to every row of df
        for key, value in metadata_values.items():
            self.df[key] = value

def docx_table_to_pd(docx_table):
    # magic code taken from https://stackoverflow.com/questions/58254609/python-docx-parse-a-table-to-panda-dataframe
    df = [['' for i in range(len(docx_table.columns))] for j in range(len(docx_table.rows))]
    for i, row in enumerate(docx_table.rows):
        for j, cell in enumerate(row.cells):
            if cell.text:
                df[i][j] = cell.text
    return pd.DataFrame(df)
