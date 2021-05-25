# Variant 21
# Spivac Iana FAF-192

# Vn = ['S', 'B', 'D', 'A']
# Vt = ['f', 'c', 'g', 'd']
# P = ["S->BfD", "B->Bc", "B->D", "D->Ag", "D->A", "A->d","A->c"]
# word = "dgcfdg"

Vn = ['S', 'F', 'L', 'E']
Vt = ['a', 'b', 'c', 'd','e']
P = ["S->LdF", "F->E", "L->ca", "L->La", "E->b", "E->Eeb"]
word = "caadbeb"

states = {}
first = {}
last = {}
precedenceMatrix = {}
allSymbols = Vn + Vt
allSymbols.append('$')

def readInput():
    for el in P:
        symbols = []
        if el[0] not in states.keys(): states[el[0]] = []
        for symbol in el:
            if symbol != '-' and symbol != '>':
                symbols.append(symbol)
        states[symbols.pop(0)].append(symbols)


def addFirstLast(leftSide, reccurentLeftSide, pos, dict):
    #adding the first/last term which occurs in production, if it's a non-terminal
    #a reccurence will occur
    for rightSide in states[reccurentLeftSide]:
        if rightSide[pos] not in dict[leftSide]:
            dict[leftSide].append(rightSide[pos])
            if rightSide[pos] in Vn:
                addFirstLast(leftSide, rightSide[pos], pos, dict)


def firstLast():
    for nonTerminal in Vn:
        first[nonTerminal] = []
        last[nonTerminal] = []
        addFirstLast(nonTerminal, nonTerminal, 0, first)
        addFirstLast(nonTerminal, nonTerminal, -1, last)


def rule1(production, count):
    precedenceMatrix[production[count]][production[count + 1]].append('=')


def rule2(production, count):
    if production[count + 1] in Vn:
        for symbol in first[production[count + 1]]:
            precedenceMatrix[production[count]][symbol].append('<')

def rule3(production, count):
    if production[count] in Vn and production[count + 1] in Vt:
        for symbol in last[production[count]]:
            precedenceMatrix[symbol][production[count + 1]].append('>')
    elif production[count] in Vn and production[count + 1] in Vn:
        #does this even work?
        for symbol in last[production[count]]:
            for symbol2 in first[production[count + 1]]:
                if symbol2 in Vt:
                    precedenceMatrix[symbol][symbol2].append('>')

def initializeMatrix(array):
    for el in array:
        precedenceMatrix[el] = {}
        for element in array:
            precedenceMatrix[el][element] = []
            if el == '$' and element != '$':
                precedenceMatrix['$'][element] = ['<']
        if el != '$':
            precedenceMatrix[el]['$'] = ['>']

def completeMatrix(dict):
    initializeMatrix(allSymbols)
    for leftSide, rightSide in dict.items():
        for production in rightSide:
            if len(production) > 1:
                count = 0
                while (count < len(production) - 1):
                    rule1(production, count)
                    rule2(production, count)
                    rule3(production, count)
                    count += 1

def printMatrix(matrix):
    print("{:<3}".format(' '), end=' ')
    for element in allSymbols:
        print("{:<3}".format(element), end=' ')
    for element, arrayElement in matrix.items():
        print("\n{:<3}".format(element), end=' ')
        for symbol in arrayElement:
            if (len(arrayElement[symbol]) == 0):
                print("{:<3}".format(' '), end=' ')
            else:
                print("{:<3}".format(arrayElement[symbol][0]), end=' ')
    print()

def replaceTerm(symbols):
    for leftSide, rightSide in states.items():
        if symbols in rightSide:
            return ["<",leftSide,">"]

def printParse(array):
    for term in array:
        print(term, end="")
    print()

def verifyInput(input, matrix):
    symbols=[]
    newInput=["$"]
    i=1
    while input[i] != "$":
        if input[i] == "<":
            i +=1
            start = i-1
            symbols=[]
            #while it isn't closing it will make the neccesar operations
            while input[i] != ">":
                if input[i] == "<":
                    #if "<" occurs it means it shall abort current opening "<" and get to next
                    for j in range(start,i):
                        newInput.append(input[j])
                    symbols=[]
                    i -=1
                    break
                if input[i] in allSymbols:
                    #adding all terms between "<" and ">"
                    symbols.append(input[i])
                i += 1
            i += 1
            if len(symbols) == 1:
                if input[i] != '$':
                    #if one term has connection "=" on its right side
                    if matrix[input[i-2]][input[i]][0] == "=":
                        newInput.extend(["<",input[i-2],"="])
                    # if one term has connection "=" on its left side
                    elif matrix[input[i - 4]][input[i-2]][0] == "=":
                        newInput.extend(["=",input[i-4],">"])
                    else:
                        newInput.extend(replaceTerm(symbols))
                #else if it's "$"
                else:
                    if matrix[input[start-1]][input[start+1]][0] == "=":
                        newInput.extend(["=",input[start+1],">"])
                    else:
                        newInput.extend(replaceTerm(symbols))
            elif len(symbols) > 0:
                newInput.append("<")
                for leftSide, rightSide in states.items():
                    if symbols in rightSide:
                        newInput.append(leftSide)
                        newInput.append(">")
        else:
            newInput.append(input[i])
            i += 1
    newInput.append("$")
    printParse(newInput)
    #recurence will occur while single "S" with additional symbols($,<,>) will not remain
    if len(newInput) > 5:
        verifyInput(newInput, matrix)


def parseInput(input, matrix):
    inputList = []
    #adding to matrix symbols
    for i in range(0, (len(input) - 1) * 2, 2):
        input = input[:i + 1] + matrix[input[i]][input[i + 1]][0] + input[i + 1:]
    #turning input string to list
    for symbol in input:
        inputList.append(symbol)
    verifyInput(inputList, matrix)

readInput()
firstLast()
completeMatrix(states)
printMatrix(precedenceMatrix)
parseInput("$" + word + "$", precedenceMatrix)
