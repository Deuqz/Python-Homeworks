from functools import reduce
import operator


def makeTemplate(table):
    return "{ |" + " l |" * len(table[0]) + " }"


def makeCell(elem):
    return " & " + str(elem)


def getTableRow(row):
    return str(row[0]) + reduce(operator.add, map(makeCell, row[1:])) + "\\\\ \\hline\n"


def createLatexTable(table):
    with open("artifacts/table.tex", 'w') as file:
        file.write("\\documentclass{article}\n" \
                   "\\usepackage[utf8]{inputenc}\n" \
                   "\\title{Table}\n" \
                   "\\begin{document}\n" \
                   "\\maketitle\n" \
                   "\\begin{tabular}" \
                   + makeTemplate(table) + "\n\\hline\n" \
                   + reduce(operator.add, map(getTableRow, table)) + "\\end{tabular}\n" \
                                                                     "\\end{document}")