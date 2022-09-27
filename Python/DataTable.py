import pandas as pd
import numpy as np
from camelot import read_pdf, plot
from docx import Document, table
import os
import errno
import tkinter as tk
from tkinter import filedialog


MEASURES_HEADERS = ["#", "Recovery measures"]
INDEX_HEADER = "#"
JOIN_HEADER = "Recovery measures"
METADATA_HEADERS = ["Species name", "Designatable Unit", "Taxon", "COSEWIC Status", "SARA Status", "Lead Region"]


class TableDoc:
    """ Either a Resdoc, recovery plan or action plan document containing
    tabular data to parse and save.
    """

    def __init__(self, doc_file_path=None):
        self.metadata_dict = {}
        self.doc_path = ""
        self.dt_list = []  # doc table list
        self.measures_list = []
        self.out_dt = None

        # make sure the filepath exists and is either a pdf or a Word doc:
        if not doc_file_path:
            root = tk.Tk()
            root.withdraw()
            doc_file_path = filedialog.askopenfilename()

        if not os.path.isfile(doc_file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), doc_file_path)
        elif not doc_file_path.endswith((".doc", ".docx", ".pdf")):
            raise Exception("File type not supported, must be PDF or Word document.")
        else:
            self.doc_path = doc_file_path

        self.scrape_doc()
        self.join_data()

    def scrape_doc(self):
        # checks if doc is word or pdf and scrapes it accordingly
        if self.doc_path.endswith((".doc", ".docx")):
            self.scrape_word()
        elif self.doc_path.endswith(".pdf"):
            self.scrape_pdf()
        else:
            raise Exception("File type not supported, must be PDF or Word document.")

    def scrape_pdf(self, line_scale=50):
        self.dt_list = read_pdf(self.doc_path, pages="all", line_scale=line_scale)

    def scrape_word(self):
        # function that extracts all the tables from a Word doc and saves them to self.dt_list as DocTable objects
        recovery_docx = Document(self.doc_path)
        self.dt_list = [DocTable(raw_table) for raw_table in recovery_docx.tables]
        self.dt_list = [dt for dt in self.dt_list if dt.is_valid]
        self.measures_list = [dt for dt in self.dt_list if dt.is_measures_table]

    def get_metadata(self):
        # TODO
        # either extracts the metadata table from the doc, or takes input parameters, should set class values
        pass

    def join_data(self):
        # loops through self.measures_list and converts all the tables into a single output, ready for writting into an
        # excel/etc.
        if len(self.measures_list):
            self.out_dt = self.measures_list[0]
            for measure_dt in self.measures_list[1:]:
                self.out_dt.merge_tables(measure_dt.df)

    def write_to_excel(self, outpath):
        # TODO
        # Writes the output df into an excel sheet and returns with the whole sheet, or the pathname.
        # settings.BASE_DIR
        # figure out the filename
        self.out_dt.df.to_excel(outpath, index=False)
        os.startfile(outpath)


    def show_grid_lines(self, table_index):
        # shows the grid lines for camelot tables, useful for debugging
        return plot(self.df_list[table_index], kind='grid').show()

    def parser_report(self, table_index):
        # shows the report for a camelot table, may be useful for QC
        return self.df_list[table_index].parsing_report


class DocTable:
    """ An individual table as extracted from the document in DocTable
    """

    def __init__(self, raw_table):
        self.df = pd.DataFrame()
        self.is_valid = True  # is this a valid table with data?
        self.is_measures_table = False  # does this table contain recovery measures?
        self.is_metadata_table = False  # does this table contain metadata?

        # upon init, the input datatable should get cleaned, classified and stored as a class attribute
        # should also handle the empty table case i.e. raw_table = None
        if raw_table is not None and type(raw_table) == table.Table:
            self.df = docx_table_to_pd(raw_table)
            self.clean()

    def clean(self):
        # The input table should be converted into a pd dataframe, with various checks to set flags
        # remove regex values
        self.df = self.df.replace(r'\r+|\n+|\t+', '', regex=True)
        self.df = self.df.replace('', np.nan)
        self.set_headers()
        self.set_table_type()

        self.is_valid = True

    def set_headers(self):
        # set the first row as the column headers, code from:
        # https://stackoverflow.com/questions/31328861/python-pandas-replacing-header-with-top-row
        new_header = self.df.iloc[0]  # grab the first row for the header
        self.df = self.df[1:]  # take the data less the header row
        self.df.columns = new_header  # set the header row as the df header

    def set_table_type(self):
        # sets the flag and drops any uneeded columns
        if all([mh in self.df.columns for mh in MEASURES_HEADERS]):
            self.is_measures_table = True
            self.df = self.df[MEASURES_HEADERS]

        if all([mh in self.df.columns for mh in METADATA_HEADERS]):
            self.is_metadata_table = True
            self.df = self.df[METADATA_HEADERS]

    def merge_tables(self, df_to_merge):
        # Merge this table with another valid DocTable
        # look into this to merge rows split over pages:
        # https://stackoverflow.com/questions/40733386/python-pandas-merge-rows-if-some-values-are-blank
        self.df = pd.concat([self.df, df_to_merge], axis=0)
        # forward fill in any empty index column values:
        self.df.loc[:, INDEX_HEADER] = self.df.loc[:, INDEX_HEADER].ffill()
        self.df = self.df.groupby([INDEX_HEADER], as_index=False, sort=False)[JOIN_HEADER].apply(lambda x: ' '.join(x.astype(str)))

    def add_metadata(self, metadata_values):
        # TODO
        # given some metadata, add those columns to every row of df
        pass


def docx_table_to_pd(docx_table):
    # magic code taken from https://stackoverflow.com/questions/58254609/python-docx-parse-a-table-to-panda-dataframe
    df = [['' for i in range(len(docx_table.columns))] for j in range(len(docx_table.rows))]
    for i, row in enumerate(docx_table.rows):
        for j, cell in enumerate(row.cells):
            if cell.text:
                df[i][j] = cell.text
    return pd.DataFrame(df)
