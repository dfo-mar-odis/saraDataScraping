import pandas as pd
from camelot import read_pdf, plot
from docx import Document


class TableDoc:
    """ Either a Resdoc, recovery plan or action plan document containing
    tabular data to parse and save.
    """

    doc_path = ""
    df_list = []

    def __init__(self, doc_file_path):
        self.doc_path = doc_file_path

    def scrape_pdf(self, *args, **kwargs):
        # line_scale = 50 is useful
        self.df_list = read_pdf(self.doc_path, pages="all", *args, **kwargs)

    def scrape_word(self, *args, **kwargs):
        # TODO
        # function that extracts all the tables from a word doc and saves them to self.df_list
        recovery_docx = Document(self.doc_path)
        self.df_list = "foo"

    def scrape_doc(self):
        # TODO
        # checks if doc is word or pdf and scrapes it accordingly
        pass

    def get_metadata(self):
        # TODO
        # either extracts the metadata table from the doc, or takes input parameters, should set class values
        pass

    def join_data(self):
        # TODO
        # loops through self.df_list and converts all the tables into a single output, ready for writting into an
        # excel/etc.
        pass

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
    df = pd.DataFrame()

    def __init__(self, dataTable):
        # TODO
        # upon init, the input datatable should get stored as a class attribute
        pass

    def clean(self):
        # TODO
        # The input table should be converted into a pd dataframe, with various checks
        # is it empty?
        # do the headers match?
        # etc.
        pass

    def set_headers(self):
        # TODO
        # set the first row as the column headers
        pass

    def merge_tables(self, table_to_merge):
        # TODO
        # Merge this table with another valid DocTable
        pass

    def add_metadata(self, metadata_values):
        # TODO
        # given some metadata, add those columns to every row of df
        pass
