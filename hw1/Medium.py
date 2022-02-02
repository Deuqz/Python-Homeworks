import networkx as nx
import matplotlib.pyplot as plt
import ast

numArgs = 0
numBody = 0
numIf = 0
numElse = 0
numComp = 0
numRet = 0
numList = 0
numOp = 0
numBinOp = 0
numCallsFunc = 0
numAttr = 0
numSubscrts = 0
numExpr = 0
numFor = 0


def createGraph(v, g, add_name=""):
    global numArgs
    global numBody
    global numIf
    global numElse
    global numComp
    global numRet
    global numList
    global numOp
    global numBinOp
    global numCallsFunc
    global numAttr
    global numSubscrts
    global numFor
    # print(type(v))
    name = "ERROR"
    if type(v) == ast.FunctionDef:
        name = "Function:" + v.name
        g.add_node(name)
        node1 = createGraph(v.args, g)
        g.add_edge(name, node1)
        for u in v.body:
            node2 = createGraph(u, g)
            g.add_edge(name, node2)
    elif type(v) == ast.arguments:
        name = "Args " + str(numArgs)
        numArgs += 1
        for u in v.args:
            node = createGraph(u, g)
            g.add_edge(name, node)
    elif type(v) == ast.arg:
        name = str(v.arg)
    elif type(v) == ast.If:
        name = "if " + str(numIf)
        numIf += 1
        node1 = createGraph(v.test, g)
        g.add_edge(name, node1)
        nodeBody = "Body " + str(numBody)
        numBody += 1
        g.add_edge(name, nodeBody)
        for u in v.body:
            node2 = createGraph(u, g)
            g.add_edge(nodeBody, node2)
        nodeElse = "else " + str(numElse)
        numElse += 1
        g.add_edge(name, nodeElse)
        for u in v.orelse:
            node3 = createGraph(u, g)
            g.add_edge(nodeElse, node3)
    elif type(v) == ast.Compare:
        name = "compare " + str(numComp)
        numComp += 1
        node1 = createGraph(v.left, g, "left: ")
        g.add_edge(name, node1)
        node2 = createGraph(v.ops[0], g, "op: ")
        g.add_edge(name, node2)
        node3 = createGraph(v.comparators[0], g, "right: ")
        g.add_edge(name, node3)
    elif type(v) == ast.Constant:
        name = add_name + str(v.value)
        g.add_node(name)
    elif type(v) == ast.Name:
        name = add_name + str(v.id)
        g.add_node(name)
    elif type(v) == ast.Return:
        name = "return " + str(numRet)
        numRet += 1
        node = createGraph(v.value, g)
        g.add_edge(name, node)
    elif type(v) == ast.List:
        name = "list " + str(numList)
        numList += 1
        for u in v.elts:
            node = createGraph(u, g)
            g.add_edge(name, node)
    elif type(v) == ast.Assign:
        name = add_name + "=" + str(numOp)
        numOp += 1
        for u in v.targets:
            node1 = createGraph(u, g, "left: ")
            g.add_edge(name, node1)
        node2 = createGraph(v.value, g, "right: ")
        g.add_edge(name, node2)
    elif type(v) == ast.BinOp:
        name = add_name + "binOp " + str(numBinOp)
        numBinOp += 1
        node1 = createGraph(v.left, g, "left: ")
        g.add_edge(name, node1)
        node2 = createGraph(v.op, g, "op: ")
        g.add_edge(name, node2)
        node3 = createGraph(v.right, g, "right: ")
        g.add_edge(name, node3)
    elif type(v) == ast.Call:
        name = "call function " + str(numCallsFunc)
        numCallsFunc += 1
        node1 = createGraph(v.func, g)
        g.add_edge(name, node1)
        nodeArgs = "Args" + str(numArgs)
        numArgs += 1
        g.add_edge(name, nodeArgs)
        for u in v.args:
            node2 = createGraph(u, g)
            g.add_edge(nodeArgs, node2)
    elif type(v) == ast.Attribute:
        name = "attribute" + str(numAttr)
        numAttr += 1
        node1 = createGraph(v.value, g)
        g.add_edge(name, node1)
        g.add_edge(name, str(v.attr))
    elif type(v) == ast.Subscript:
        name = "subscript" + str(numSubscrts)
        numSubscrts += 1
        node1 = createGraph(v.value, g, "name: ")
        g.add_edge(name, node1)
        node2 = createGraph(v.slice, g, "ind: ")
        g.add_edge(name, node2)
    elif type(v) == ast.UnaryOp:
        if type(v.op) == ast.USub:
            name = createGraph(v.operand, g, add_name + "-")
    elif type(v) == ast.Expr:
        name = "expr" + str(numExpr)
        numFor += 1
        node = createGraph(v.value, g)
        g.add_edge(name, node)
    elif type(v) == ast.For:
        name = "for " + str(numFor)
        numFor += 1
        nodeVar = createGraph(v.target, g)
        g.add_edge(name, nodeVar)
        nodeIter = createGraph(v.iter, g)
        g.add_edge(name, nodeIter)
        nodeBody = "Body " + str(numBody)
        numBody += 1
        g.add_edge(name, nodeBody)
        for u in v.body:
            node = createGraph(u, g)
            g.add_edge(nodeBody, node)
    elif type(v) == ast.LtE:
        name = add_name + "<=" + str(numOp)
        g.add_node(name)
    elif type(v) == ast.Eq:
        name = add_name + "==" + str(numOp)
        g.add_node(name)
    elif type(v) == ast.Sub:
        name = add_name + "-" + str(numOp)
        g.add_node(name)
    elif type(v) == ast.Add:
        name = add_name + "+" + str(numOp)
        g.add_node(name)
    if name == "ERROR":
        raise Exception
    return name


def showGraph():
    file = ""
    with open("Easy.py", 'r') as f:
        file = f.read()
    ast_obj = ast.parse(file)
    graph = nx.DiGraph()
    ver = ast_obj.body[0]
    createGraph(ver, graph)
    subax = plt.subplot(121)
    nx.draw(graph, with_labels=True)
    plt.show()
    nx.draw(graph, with_labels=True)
    fig = plt.gcf()
    fig.set_size_inches(10, 10)
    fig.savefig('artifacts/graph.png')
