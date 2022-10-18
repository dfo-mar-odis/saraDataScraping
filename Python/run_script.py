import Python.DataTable as dt
res_doc = dt.TableDoc()
res_doc.write_to_excel("..\\temp\\out.xlsx")

#Playing with code
if False:
    print(res_doc.doc_path)
    res_doc.scrape_word()
    res_doc.measures_list
    res_doc.join_data()
    res_doc.measures_list[0].set_table_type()