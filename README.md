# Extracting recovery measures information from Recovery Documents using Reproducible Analytical Pipelines and identifying best practices for future data entry and reporting

The project is focused on enabling SARP to test how to efficiently and accurately extract text from Recovery Documents, SARA workplans, and Progress Reports to automatically transfer the written text in these documents into designated cells in a spreadsheet to populate a final database. This workflow will then be used to develop workflows to explore the process of generating reproducible reports.

Outcomes of this project will include:

1.  Testing and evaluating the use of Reproducible Analytical Pipelines to automate data extraction from SARA recovery documents and Species at Risk geodatabase.
2.  Make recommendations regarding document elements (e.g. formatting or codes) required to identify and extract relevant information into a spreadsheet. This will coincide with the Species at Risk Program recovery and implementation team plans to revise Species' Progress Report templates and other recovery document templates this fiscal year.
3.  Conceptual workflow of elements that would be required to reverse-engineer outcomes 1 and 2 (above) by using forms, csv files, or Excel spreadsheets to generate reproducible reports (e.g. using Microsoft PowerBI, R Markdown, or other tools that are easily used and accessible to Species at Risk Program staff).

## Handy Links:
 - Detailed instructions for getting the workflow up and running can be found [here](https://086gc-my.sharepoint.com/:w:/g/personal/quentin_stoyel_dfo-mpo_gc_ca/EXCqIsufb5tHpf1tW7dskL8BBj6BbBfMdY2Wan8rserOeg?e=BCpalP).

-   Project board to craft, coordinate, and track milestones to be completed throughout the duration of this project: <https://github.com/orgs/dfo-mar-odis/projects/2/views/14> Most of the work of this project will be coordinated asynchronously through this board (which will be linked to the code to be developed), in addition to monthly meetings. The link above is for a for a view specifically for this project, however, the board contains other views for additional projects of the Reproducible Analytical Pipeline initiative.
-   SARP documents: This project will select and review a list of SARP documents to extract data from, and identify the type of information to be standardized and extracted. The following link contains a folder that lists potential documents to be reviewed: [folder](https://086gc.sharepoint.com/:f:/s/MaritimesSpatialPlanning-MAROpenDataLogistics/Ej_hnfwCzfdEnlzCpE2jBXwB1DM6zJEToE9rmaPJxWy84w?e=pJJXxB)


### Project Folder
- SARP documents: This project will select and review a list of SARP documents to extract data from, and identify the type of information to be standardized and extracted. The following link contains a folder that lists documents to be tested, as provided by Sam: [folder](https://086gc.sharepoint.com/:f:/s/MaritimesSpatialPlanning-MAROpenDataLogistics/EvvcRBMcJSpHkfjg2lMPfSgBzyATiN5JYVJtqH92j5CCaA?e=d1nVCT).

### Project Proposal
- Full description of this project is available in a protected SharePoint file: [full project text](https://086gc.sharepoint.com/:w:/s/MaritimesSpatialPlanning-MAROpenDataLogistics/EZLu-2jTNt1DgVY_0GsX3eEBtsJwi7xA_vWNSAqwBURbdg?e=qzbbf0)

## R Installation

``` r
install.packages("remotes")
remotes::install_deps()
```

Adding a package:

``` r
usethis::use_package("packageName")
```

After adding a new package, commit the updated description file to source control.

## Python Installation

Create a virtual environment, in terminal: `python -m venv venv`

Activate it (`source venv/bin/activate`), or select it as the python interpreter under project options.

Install the needed packages: `pip install -r requirements.txt`
