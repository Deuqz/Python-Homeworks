import networkx as nx
import matplotlib.pyplot as plt
import ast


num = 0
names = dict()
g = nx.DiGraph()

def createGraph(v, add_name=""):
    global num
    global names
    global g
    curNum = num
    num += 1
    if type(v) == ast.FunctionDef:
        names[curNum] = "Function:" + v.name
        g.add_node(curNum)
        numNode1 = createGraph(v.args)
        g.add_edge(curNum, numNode1)
        for u in v.body:
            numNode2 = createGraph(u)
            g.add_edge(curNum, numNode2)
    elif type(v) == ast.arguments:
        names[curNum] = "Args"
        for u in v.args:
            numNode = createGraph(u)
            g.add_edge(curNum, numNode)
    elif type(v) == ast.arg:
        names[curNum] = str(v.arg)
        g.add_node(curNum)
    elif type(v) == ast.If:
        names[curNum] = "If"
        numNode1 = createGraph(v.test)
        g.add_edge(curNum, numNode1)
        numNodeBody = num
        num += 1
        names[numNodeBody] = "Body"
        g.add_edge(curNum, numNodeBody)
        for u in v.body:
            numNode2 = createGraph(u)
            g.add_edge(numNodeBody, numNode2)
        numNodeElse = num
        num += 1
        names[numNodeElse] = "else"
        g.add_edge(curNum, numNodeElse)
        for u in v.orelse:
            numNode3 = createGraph(u)
            g.add_edge(numNodeElse, numNode3)
    elif type(v) == ast.Compare:
        names[curNum] = "Compare"
        numNode1 = createGraph(v.left, "left: ")
        g.add_edge(curNum, numNode1)
        numNode2 = createGraph(v.ops[0], "op: ")
        g.add_edge(curNum, numNode2)
        numNode3 = createGraph(v.comparators[0], "right: ")
        g.add_edge(curNum, numNode3)
    elif type(v) == ast.Constant:
        names[curNum] = add_name + str(v.value)
        g.add_node(curNum)
    elif type(v) == ast.Name:
        names[curNum] = add_name + str(v.id)
        g.add_node(curNum)
    elif type(v) == ast.Return:
        names[curNum] = "Return"
        numNode = createGraph(v.value)
        g.add_edge(curNum, numNode)
    elif type(v) == ast.List:
        names[curNum] = "List"
        for u in v.elts:
            numNode = createGraph(u)
            g.add_edge(curNum, numNode)
    elif type(v) == ast.Assign:
        names[curNum] = add_name + "="
        for u in v.targets:
            numNode1 = createGraph(u, "left: ")
            g.add_edge(curNum, numNode1)
        numNode2 = createGraph(v.value, "right: ")
        g.add_edge(curNum, numNode2)
    elif type(v) == ast.BinOp:
        names[curNum] = add_name + "BinOp"
        numNode1 = createGraph(v.left, "left: ")
        g.add_edge(curNum, numNode1)
        numNode2 = createGraph(v.op, "op: ")
        g.add_edge(curNum, numNode2)
        numNode3 = createGraph(v.right, "right: ")
        g.add_edge(curNum, numNode3)
    elif type(v) == ast.Call:
        names[curNum] = "Call function"
        numNode1 = createGraph(v.func)
        g.add_edge(curNum, numNode1)
        numNodeArgs = num
        num += 1
        names[numNodeArgs] = "Args"
        g.add_edge(curNum, numNodeArgs)
        for u in v.args:
            numNode2 = createGraph(u)
            g.add_edge(numNodeArgs, numNode2)
    elif type(v) == ast.Attribute:
        names[curNum] = "Attribute"
        numNode1 = createGraph(v.value)
        g.add_edge(curNum, numNode1)
        numNode2 = num
        num += 1
        names[numNode2] = str(v.attr)
        g.add_edge(curNum, numNode2)
    elif type(v) == ast.Subscript:
        names[curNum] = "Subscript"
        numNode1 = createGraph(v.value, "name: ")
        g.add_edge(curNum, numNode1)
        numNode2 = createGraph(v.slice, "ind: ")
        g.add_edge(curNum, numNode2)
    elif type(v) == ast.UnaryOp:
        if type(v.op) == ast.USub:
            curNum = createGraph(v.operand, add_name + "-")
    elif type(v) == ast.Expr:
        names[curNum] = "Expr"
        numNode = createGraph(v.value)
        g.add_edge(curNum, numNode)
    elif type(v) == ast.For:
        names[curNum] = "for"
        numNodeVar = createGraph(v.target)
        g.add_edge(curNum, numNodeVar)
        numNodeIter = createGraph(v.iter)
        g.add_edge(curNum, numNodeIter)
        numNodeBody = num
        num += 1
        names[numNodeBody] = "Body"
        g.add_edge(curNum, numNodeBody)
        for u in v.body:
            numNode = createGraph(u)
            g.add_edge(numNodeBody, numNode)
    elif type(v) == ast.LtE:
        names[curNum] = add_name + "<="
        g.add_node(curNum)
    elif type(v) == ast.Eq:
        names[curNum] = add_name + "=="
        g.add_node(curNum)
    elif type(v) == ast.Sub:
        names[curNum] = add_name + "-"
        g.add_node(curNum)
    elif type(v) == ast.Add:
        names[curNum] = add_name + "+"
        g.add_node(curNum)
    return curNum


def showGraph():
    file = ""
    with open("Easy.py", 'r') as f:
        file = f.read()
    ast_obj = ast.parse(file)
    createGraph(ast_obj.body[0])
    subax = plt.subplot(121)
    nx.draw(g, with_labels=True, labels=names)
    fig = plt.gcf()
    fig.set_size_inches(20, 15)
    fig.savefig('artifacts/graph.pdf')
