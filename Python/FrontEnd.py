import pandas as pd
from tkinter import *
from tkinter import filedialog


class TkGui:
    def __init__(self):
        self.table_doc_path = ""
        self.metadata_dict = {}

        self.master_index_dict = {}
        self.masterlist_df = pd.DataFrame()

        self.master = Tk()
        self.master.geometry("400x400")

        self.master.title("SAR Data Scraper")

        # vars:
        masterlist_button = Button(self.master, text="Select SAR masterlist", command=self.set_masterlist)
        masterlist_button.pack()

        self.species_dropdown = StringVar(self.master)
        self.species_option_menu = OptionMenu(self.master, self.species_dropdown, [])
        self.species_dropdown.trace("w", self.set_masterlist_metadata)

        self.species_option_menu.pack()

        table_doc_button = Button(self.master, text="Select SAR Document", command=self.set_table_doc_path)
        table_doc_button.pack()
        self.master.mainloop()
        # gui gets closed in set_table_doc_path method, once path is obtained.

    def set_masterlist(self):
        masterlist_path = filedialog.askopenfilename()
        if masterlist_path:
            try:
                self.masterlist_df = pd.read_csv(masterlist_path)
                self.masterlist_df["dropdown_text"] = self.masterlist_df["COMMON_E"] + ", " + self.masterlist_df["POP_E"] + " population. (" + \
                                    self.masterlist_df["LEAD_REG_E"] + ")"

                self.master_index_dict = {v: k for k, v in self.masterlist_df['dropdown_text'].to_dict().items()}
                self._reset_option_menu(self.master_index_dict.keys())
            except:
                raise Exception("Invalid masterlist selected. Should be a .csv take from SARA SDE")

    def set_masterlist_metadata(self, *args):
        if self.species_dropdown.get() in self.master_index_dict.keys():
            self.metadata_dict = self.masterlist_df.loc[[self.master_index_dict[self.species_dropdown.get()]]].to_dict('records')[0]

    def set_table_doc_path(self):
        self.table_doc_path = filedialog.askopenfilename()
        self.master.destroy()
        print("Frontend closed gracefully")

    def _reset_option_menu(self, options):
        """reset the values in the option menu
        if index is given, set the value of the menu to
        the option at the given index
        """
        menu = self.species_option_menu["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string,
                             command=lambda value=string:
                             self.species_dropdown.set(value))
