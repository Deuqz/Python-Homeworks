from hw_python_show_graph_lib import showGraph
from Easy import getLatexTable
import os

def createLatexDocWithTableAndPicture(table):
    showGraph()
    with open("artifacts/table_and_picture.tex", 'w') as file:
        file.write("\\documentclass{article}\n"
                   "\\usepackage[utf8]{inputenc}\n"
                   "\\usepackage{graphicx}\n"
                   "\\graphicspath{{artifacts}}\n"
                   "\\DeclareGraphicsExtensions{.pdf,.png,.jpg}\n"
                   "\\title{Table and Picture}\n"
                   "\\begin{document}\n"
                   "\\maketitle\n"
                   + getLatexTable(table) +
                   "\\includegraphics[scale=0.3]{graph.png}\n"
                   "\\end{document}")


def createPDFwithTableAndPicture(table):
    createLatexDocWithTableAndPicture(table)
    os.system("pdflatex artifacts/table_and_picture.tex")
    os.system("move table_and_picture.aux artifacts/table_and_picture.aux")
    os.system("move table_and_picture.log artifacts/table_and_picture.log")
    os.system("move table_and_picture.pdf artifacts/table_and_picture.pdf")