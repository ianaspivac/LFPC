# Variant 21
# Spivac Iana FAF-192

Vn = ['S', 'A', 'B', 'D']
Vt = ['c', 'f', 'd', 'g']
P = ["S->BfD", "B->Bc", "B->D", "D->Ag", "D->A", "A->d", "A->c"]

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


def verifyInput(input, matrix):
    symbols=[]
    newInput=["$"]
    i=1
    while input[i] != "$":
        if input[i] == "<":
            i +=1
            start = i
            symbols=[]
            while input[i] != ">":

                if input[i] == "<":
                    for j in range(start,i):
                        newInput.append(input[j])
                    i -= 1
                    symbols=[]
                    break
                if input[i] != "=":
                    symbols.append(input[i])
                i += 1
            i += 1
            print(symbols)

            if len(symbols) == 1:
                print(i, input[i])
                if input[i] != '$':
                    if matrix[input[i-2]][input[i]][0] == "=":
                        newInput.append("<")
                        newInput.append(input[i-2])
                        newInput.append("=")
                    elif matrix[input[i + 2]][input[i]][0] == "=":
                        newInput.append("=")
                        newInput.append(input[i+2])
                        newInput.append(">")
                    else:
                        newInput.append("<")
                        for leftSide, rightSide in states.items():
                            if symbols in rightSide:
                                newInput.append(leftSide)
                                newInput.append(">")
                    i -= 1
                else:
                    if matrix[input[start-2]][input[start]][0] == "=":
                        newInput.append("=")
                        newInput.append(input[start])
                        newInput.append(">")

            elif len(symbols) > 0:
                newInput.append("<")
                for leftSide, rightSide in states.items():
                    if symbols in rightSide:
                        newInput.append(leftSide)
                        newInput.append(">")
                i -= 1
        else:
            newInput.append(input[i])

        i += 1
    newInput.append("$")
    print(newInput)
    if len(newInput) > 5:
        newInput.append("$")
        verifyInput(newInput, matrix)
    #print(newInput)



    # symbols = []
    # newInput = ["$"]
    # i = 1
    # while input[i] != "$":
    #     if input[i] == "<":
    #         newInput.append("<")
    #         i += 1
    #         start = i
    #         symbols = []
    #         while input[i] != ">":
    #             if input[i+1] == "<":
    #                 newInput.append("<")
    #                 break
    #             if input[i]!="=":
    #                 symbols.append(input[i])
    #             i += 1
    #         if len(symbols) > 0:
    #             for leftSide, rightSide in states.items():
    #                 if symbols in rightSide:
    #                     newInput.append(leftSide)
    #                     newInput.append(matrix[leftSide][input[i+1]][0])
    #
    #                     # print(leftSide,input[start+len(symbols)+1],start+len(symbols))
    #                     # input.insert(start + 1, matrix[leftSide][input[start+len(symbols)]][0])
    #
    #     else:
    #         newInput.append(input[i])
    #     i += 1
    # if len(input) > 5:
    #     newInput.append("$")
    #     verifyInput(newInput, matrix)
    # print(newInput)


def parseInput(input, matrix):
    inputList = []
    for i in range(0, (len(input) - 1) * 2, 2):
        input = input[:i + 1] + matrix[input[i]][input[i + 1]][0] + input[i + 1:]
    for symbol in input:
        inputList.append(symbol)
    verifyInput(inputList, matrix)



readInput()
firstLast()
completeMatrix(states)
printMatrix(precedenceMatrix)
word = "dgcfdg"
parseInput("$" + word + "$", precedenceMatrix)
