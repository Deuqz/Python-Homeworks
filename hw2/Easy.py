from functools import reduce
import operator


def getTemplate(table):
    return "{ |" + " l |" * len(table[0]) + " }"


def getCell(elem):
    return " & " + str(elem)


def getLatexTableRow(row):
    return str(row[0]) + reduce(operator.add, map(getCell, row[1:])) + "\\\\ \\hline\n"


def getLatexTable(table):
    return "\\begin{tabular}" \
           + getTemplate(table) + "\n\\hline\n" \
           + reduce(operator.add, map(getLatexTableRow, table)) \
           + "\\end{tabular}\n"


def createLatexDocWithTable(table):
    with open("artifacts/table.tex", 'w') as file:
        file.write("\\documentclass{article}\n"
                   "\\usepackage[utf8]{inputenc}\n"
                   "\\title{Table}\n"
                   "\\begin{document}\n"
                   "\\maketitle\n"
                   + getLatexTable(table)
                   + "\\end{document}")
