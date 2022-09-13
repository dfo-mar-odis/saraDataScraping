import pandas as pd
from camelot import read_pdf, plot

class TableDoc():
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

    def show_grid_lines(self, table_index):
        return plot(self.df_list[table_index], kind='grid').show()

    def parse_report(self, table_index):
        return self.df_list[table_index].parsing_report

# sample use case:
# from Python.DataTable import TableDoc
# test_table = TableDoc("Rmd/Rs-PholadeTronqueeAtlMudPiddock-v00-2022Aug-Eng.docx")
# test_table = TableDoc("temp/Mp-Sowerbys-v00-2017Apr-Eng.pdf")
# test_table.scrape_pdf()
