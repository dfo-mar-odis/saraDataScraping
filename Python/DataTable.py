import pandas as pd
from camelot import read_pdf, plot
from docx import Document
import os
import errno


class TableDoc:
    """ Either a Resdoc, recovery plan or action plan document containing
    tabular data to parse and save.
    """

    def __init__(self, doc_file_path):
        self.metadata_dict = {}
        self.doc_path = ""
        self.dt_list = []  # doc table list
        self.measures_list = []
        self.out_dt = None

        # make sure the filepath exists and is either a pdf or a Word doc:

        if not os.path.isfile(doc_file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), doc_file_path)
        elif not doc_file_path.endswith((".doc", ".docx", ".pdf")):
            raise Exception("File type not supported, must be PDF or Word document.")
        else:
            self.doc_path = doc_file_path

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
        self.out_dt = DocTable(None)
        for measure_dt in self.measures_list:
            self.out_dt.merge_tables(measure_dt)

    def write_to_excel(self):
        # TODO
        # Writes the output df into an excel sheet and returns with the whole sheet, or the pathname.
        pass

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

        # TODO
        # upon init, the input datatable should get cleaned, classified and stored as a class attribute
        # should also handle the empty table case i.e. raw_table = None
        # self.df = steps_to_make_this_a_panda(raw_table)
        # self.set_headers()
        # self.clean()
        self.df = raw_table

    def clean(self):
        # TODO
        # The input table should be converted into a pd dataframe, with various checks
        # is it empty?
        # do the headers match?
        # etc.
        self.is_valid = False

    def set_headers(self):
        # TODO
        # set the first row as the column headers
        pass

    def set_table_type(self):
        # TODO
        # sets whether table is metadata or measures or other
        pass

    def merge_tables(self, table_to_merge):
        # TODO
        # Merge this table with another valid DocTable
        pass

    def add_metadata(self, metadata_values):
        # TODO
        # given some metadata, add those columns to every row of df
        pass
