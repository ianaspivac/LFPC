#Conversion Context Free Grammar to Chomsky Normal Form
#Spivac Iana FAF-192
#Variant 12
Vn = ['S', 'A', 'B', 'C', 'D']
Vt = ['a', 'b']
P = ["S->bA", "S->AC", "A->bS", "A->BC", "A->AbAa", "B->BbaA", "B->a", "B->bSA", "C->$", "D->AB"]

states = {}
states1 = {}
emptyProductions = []
productive = []
states2 = {}
states3 = {}
newStates = {}

def readInput():
    for el in P:
        symbols = []
        if el[0] not in states.keys(): states[el[0]] = []
        for symbol in el:
            if symbol != '-' and symbol != '>':
                symbols.append(symbol)
                if symbol == '$': emptyProductions.append(symbols[0])
        states[symbols.pop(0)].append(symbols)

def printProductions(dict):
    for left, right in dict.items():
        for productions in right:
            rightSide = ""
            for character in productions:
                rightSide += character
            print(left + '->' + rightSide)

def step1():
    for emptyProduction in emptyProductions:
        for leftSide, rightSide in states.items():
            states1[leftSide] = []
            for production in rightSide:
                states1[leftSide].append(production)
                i = 0
                positionsEmpty = []
                newRightSide = []
                # getting the position of the empty non-terminal
                for character in production:
                    if character == '$': states1[leftSide].remove(production)
                    if character == emptyProduction: positionsEmpty.append(i)
                    i += 1
                if len(positionsEmpty) > 1:
                    for element in production:
                        if element != emptyProduction: newRightSide.append(element)
                    states1[leftSide].append(newRightSide)
                # getting all characters except empty non-terminal
                # (everytime in this loop a different position will be omitted) and form new productions
                for positionEmpty in positionsEmpty:
                    newRightSide = []
                    for element in range(0, len(production), 1):
                        if element != positionEmpty: newRightSide.append(production[element])
                    states1[leftSide].append(newRightSide)

def addingProductions(leftSide, key):
    for i in range(0, len(states1[key]), 1):
        if states1[key][i] not in states1[leftSide]:
            states1[leftSide].append(states1[key][i])

def step2():
    for leftSide, rightSide in states1.items():
        for productions in rightSide:
            for character in productions:
                #if there is only one non terminal on right, the productions of it will be
                #added to current state on left
                if character in Vn and len(productions) == 1:
                    addingProductions(leftSide, character)
                    #getting rid of that production
                    states1[leftSide].remove(productions)

def findNonReccurence(nonTerminal):
    for leftSide, rightSide in states1.items():
        for productions in rightSide:
            for character in productions:
                #next productive non terminal is found
                if character == nonTerminal and leftSide not in productive:
                    productive.append(leftSide)
                    return findNonReccurence(leftSide)

def findProductive():
    for leftSide, rightSide in states1.items():
        for productions in rightSide:
            nrCharacters = 0
            #if production on right has terminal
            for character in productions:
                if character in Vt:
                    nrCharacters += 1
            #and all production on right consist of terminals
            if nrCharacters == len(productions):
                #the right side for sure in productive
                productive.append(leftSide)
                #and other productions containing this right side, should be verified
                findNonReccurence(leftSide)

def removeProductions(array):
    #removing productions which consist of nonProductive
    for element in array:
        for leftSide, rightSide in states1.items():
            for productions in rightSide:
                for character in productions:
                    if character == element:
                        states1[leftSide].remove(productions)
                        break

def step3():
    findProductive()
    nonProductive = []
    for element in Vn:
        if element not in productive: nonProductive.append(element)
    removeProductions(nonProductive)
    for element in nonProductive: states1.pop(element)

def isInaccesible(element):
    #element here represents the non terminal, so if no productions are containg it
    #it will be marked and the productions of it will be removed
    for leftSide, rightSide in states1.items():
        for productions in rightSide:
            for character in productions:
                if character == element: return False
    return True

def step4():
    for element in list(states1):
        if isInaccesible(element):
            del states1[element]

def appendProduction(dict,arrayAppend,left):
    dict[left] = []
    dict[left].append(arrayAppend)

def conversionTerminals():
    i = 1
    for element in Vt:
        oldChar = element
        element = "X" + str(i)
        appendProduction(states2,[oldChar],element)
        appendProduction(newStates, [oldChar], element)
        i += 1

global iteration
iteration = 1

def conversionNonTerminals(term1, term2):
    global iteration
    element = "Y" + str(iteration)
    k=0
    #this loop could be written in 2 lines,but dumb interpreter kept give me an error
    for produces in newStates.values():
        if [term1, term2] in produces:
            m=0
            for key in newStates.keys():
                if(m==k):return key
                m+=1
        k+=1
    appendProduction(newStates, [term1, term2], element)
    appendProduction(states3, [term1, term2], element)
    iteration += 1
    return element

def replaceTerminals(element):
    for left, right in states2.items():
        for terminal in right:
            if terminal[0] in element: return left

def addTerminals(dict, i):
    repeat = False
    tempStates = {}
    for leftSide, rightSide in dict.items():
        for productions in rightSide:
            if len(productions) > 2:
                newState = conversionNonTerminals(productions[0], productions[1])
                productions.pop(0)
                productions[0] = newState
                if leftSide not in tempStates.keys() :
                    tempStates[leftSide] = []
                tempStates[leftSide].append(productions)
                repeat = True
            else:
                if leftSide not in states3.keys():
                    appendProduction(states3, productions, leftSide)
                elif productions not in states3[leftSide]:
                    states3[leftSide].append(productions)
    if repeat == True:
        return addTerminals(tempStates, i)

def step5():
    conversionTerminals()
    for leftSide, rightSide in states1.items():
        states2[leftSide] = []
        for productions in rightSide:
            newRightSide = []
            for element in productions:
                if element in Vt and len(productions) > 1: element = replaceTerminals(productions)
                newRightSide.append(element)
            states2[leftSide].append(newRightSide)
    addTerminals(states2, 1)

readInput()
print("Initial Context Free Grammar:")
printProductions(states1)
if len(emptyProductions) != 0:step1()
else: states1 = states
print("Getting rid of epsilon produces:")
printProductions(states1)
step2()
print("Getting rid of unit produces:")
printProductions(states1)
step3()
print("Getting rid of non-productive symbols:")
printProductions(states1)
step4()
print("Getting rid of inaccesible symbols:")
printProductions(states1)
step5()
print("The Chomsky Normal Form:")
printProductions(states3)


