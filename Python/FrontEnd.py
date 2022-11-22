import numpy as np
import tkinter.messagebox

import pandas as pd
from tkinter import *
from tkinter import filedialog
from functools import partial

from DataTable import TableDoc

masterlist_keys = {"common_name": "COMMON_E",
                   "population": "POP_E",
                   "lead_region": "LEAD_REG_E",
                   }


def write_master_list_option(df, with_population=True):

    if with_population:
        return df[masterlist_keys["common_name"]] + ", " + df[masterlist_keys["population"]] + " population. (" +df[masterlist_keys["lead_region"]] + ")"
    else:
        return df[masterlist_keys["common_name"]] + "(" + df[masterlist_keys["lead_region"]] + ")"


class TkGui:
    def __init__(self):
        self.table_doc_path = ""
        self.output_path = "..\\temp\\out.xlsx"
        self.metadata_dict = {}

        self.master_index_dict = {}
        self.masterlist_df = pd.DataFrame()

        self.doc = None
        self.final_doc = None

        self.header_dict = {"measures_headers": [],
                            "index_header": "",
                            "join_header": ""
                            }

        self.master = Tk()
        self.master.title("SAR Data Scraper")

        # --------------------- MASTERLIST FRAME ----------------
        self.masterlist_frame = LabelFrame(self.master, text="Select Species")
        self.masterlist_frame.grid(row=0, column=0, padx=20, pady=10)

        masterlist_label = Label(self.masterlist_frame, text="Select SAR Masterlist")
        masterlist_button = Button(self.masterlist_frame, text="Select file (.csv)", command=self.set_masterlist)
        masterlist_label.grid(row=0, column=0)
        masterlist_button.grid(row=1, column=0)

        species_dropdown_label = Label(self.masterlist_frame, text="Select SAR Species")
        self.species_dropdown = StringVar(self.masterlist_frame)
        self.species_option_menu = OptionMenu(self.masterlist_frame, self.species_dropdown, [])
        self.species_dropdown.trace("w", self.set_masterlist_metadata)
        species_dropdown_label.grid(row=0, column=1)
        self.species_option_menu.grid(row=1, column=1)

        self.set_padding(self.masterlist_frame)

        # ---------------------TABLEDOC FRAME ----------------
        self.tabledoc_frame = LabelFrame(self.master, text="Select Document")
        self.tabledoc_frame.grid(row=1, column=0, padx=20, pady=10)

        tabledoc_label = Label(self.tabledoc_frame, text="Select SAR Document")
        tabledoc_button = Button(self.tabledoc_frame, text="Select Document (.docx)", command=self.load_table_doc)
        tabledoc_label.grid(row=0, column=0)
        tabledoc_button.grid(row=1, column=0)

        table_dropdown_label = Label(self.tabledoc_frame, text="Select a measures table")
        self.tables_dropdown = StringVar(self.tabledoc_frame)
        self.tables_option_menu = OptionMenu(self.tabledoc_frame, self.tables_dropdown, [])
        self.tables_dropdown.trace("w", self.set_tables)
        table_dropdown_label.grid(row=0, column=1)
        self.tables_option_menu.grid(row=1, column=1)

        self.set_padding(self.tabledoc_frame)

        # --------------------- HEADERS FRAME ----------------
        self.headers_frame = LabelFrame(self.master, text="Select Table Headers")
        self.headers_frame.grid(row=2, column=0, padx=20, pady=10)

        # --------------------- BUTTONS FRAME ----------------
        self.buttons_frame = Frame(self.master)
        self.buttons_frame.grid(row=3, column=0, padx=20, pady=10)

        parse_button = Button(self.buttons_frame, text="Generate Excel", command=self.parse_final_doc)
        done_button = Button(self.buttons_frame, text="Exit", command=self.master.destroy)
        parse_button.grid(row=0, column=0, padx=10)
        done_button.grid(row=0, column=1)
        self.master.mainloop()

    def set_masterlist(self):
        masterlist_path = filedialog.askopenfilename()
        if masterlist_path:
            try:
                self.masterlist_df = pd.read_csv(masterlist_path).fillna('')

                self.masterlist_df["dropdown_text"] = np.where(self.masterlist_df[masterlist_keys["population"]],
                                                               write_master_list_option(self.masterlist_df, with_population=True),
                                                               write_master_list_option(self.masterlist_df, with_population=False))
                self.master_index_dict = {v: k for k, v in self.masterlist_df['dropdown_text'].to_dict().items()}
                self._reset_option_menu(self.master_index_dict.keys())
            except Exception as e:
                raise Exception("Invalid masterlist selected. Should be a .csv take from SARA SDE")

    def set_tables(self, *args):
        selected_string = self.tables_dropdown.get()
        try:
            header_list = eval(selected_string[selected_string.find('['):])
        except:
            # there are so many reasons the above might crash...
            raise Exception("CODE BROKEN, selected value of ({}) is causing errors. ".format(selected_string))

        self.clear_frame(self.headers_frame)
        self.header_dict = {"measures_headers": [],
                            "index_header": "",
                            "join_header": ""
                            }

        header_col_label = Label(self.headers_frame, text="Column Name")
        tickbox_col_label = Label(self.headers_frame, text="Coulmn to save?")
        join_col_label = Label(self.headers_frame, text="Coulmn to join on?")
        index_col_label = Label(self.headers_frame, text="Index Column?")
        header_col_label.grid(row=0, column=0)
        tickbox_col_label.grid(row=0, column=1)
        join_col_label.grid(row=0, column=2)
        index_col_label.grid(row=0, column=3)

        header_row = 1
        index_var = StringVar()
        for header_index, header in enumerate(header_list):
            header_label = Label(self.headers_frame, text=header)
            header_tickbox = Checkbutton(self.headers_frame, text="", command=partial(self.set_header_dict, header, "measures_headers"),
                                         onvalue="Is header", offvalue="Is not header")
            join_tickbox = Checkbutton(self.headers_frame, text="", command=partial(self.set_header_dict, header, "join_header"),
                                       onvalue="Is join header", offvalue="Is not join header")
            index_tickbox = Radiobutton(self.headers_frame, text="", command=partial(self.set_header_dict, header, "index_header"),
                                        variable=index_var, value=header)
            header_label.grid(row=header_row, column=0)
            header_tickbox.grid(row=header_row, column=1)
            join_tickbox.grid(row=header_row, column=2)
            index_tickbox.grid(row=header_row, column=3)
            header_row += 1

        self.set_padding(self.headers_frame)

    def set_header_dict(self, header, switch, *args):
        # this needs to take the value of a checkbox and update the metadata dictionary accordingly.
        if switch in ["measures_headers"]:
            if header in self.header_dict[switch]:
                self.header_dict[switch].remove(header)
            else:
                self.header_dict[switch].append(header)
        if switch in ["index_header", "join_header"]:
            if header != self.header_dict[switch]:
                self.header_dict[switch] = header

    def set_masterlist_metadata(self, *args):
        if self.species_dropdown.get() in self.master_index_dict.keys():
            self.metadata_dict = self.masterlist_df.loc[[self.master_index_dict[self.species_dropdown.get()]]].to_dict('records')[0]

    def load_table_doc(self):
        self.table_doc_path = filedialog.askopenfilename()
        self.doc = TableDoc(self.table_doc_path)
        new_table_options = ["Table {}: {}".format(ind, dt.df.columns.to_list()) for ind, dt in enumerate(self.doc.dt_list)]
        self._reset_tables_dropdown(new_table_options)

    def parse_final_doc(self):
        self.final_doc = TableDoc(self.table_doc_path, metadata_dict=self.metadata_dict, header_dict=self.header_dict)
        try:
            self.final_doc.write_to_excel(self.output_path)
        except PermissionError:
            tkinter.messagebox.showinfo("Error", "Close the excel sheet.")

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

    def _reset_tables_dropdown(self, options):
        """reset the values in the option menu
        if index is given, set the value of the menu to
        the option at the given index
        """
        menu = self.tables_option_menu["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string,
                             command=lambda value=string:
                             self.tables_dropdown.set(value))


    def set_padding(self, frame_to_pad):
        for widget in frame_to_pad.winfo_children():
            widget.grid_configure(padx=10, pady=5)

    def clear_frame(self, frame_to_clear):
        for widget in frame_to_clear.winfo_children():
            widget.destroy()