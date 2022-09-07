# going to put the data table class in here!

import pandas as pd
from tabula import read_pdf


class TableDoc():
    """ Either a Resdoc, recovery plan or action plan document containing
    tabular data to parse and save.
    """

    doc_path = ""
    df_list = []

    def __init__(self, doc_file_path):
        super TableDoc_()
        self.doc_path = doc_file_path

    def scrape_pdf(self):
        self.df_list = read_pdf(self.doc_file_path)
