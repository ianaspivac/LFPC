# Variant 12
# Spivac Iana FAF-192

# Grammar input
Vn = ['S', 'F', 'D']
Vt = ["a", "b", "c"]
P = ["S=aF", "F=bF", "F=cD", "S=bS", "D=cS", "D=a$", "F=a$"]
#acbba
# defining states
# state which leads to a pair of accepted states and their input
states = {}
for el in P:
    if el[0] not in states.keys():
        states[el[0]] = []
    states[el[0]].append([el[-2], el[-1]])
print(states)
def verify(state, j):
    # a - state input, b - accepted state
    for a, b in state:
        # compares one input symbol with existing inputs in state
        if charList[j] == a:
            # verify if the last input symbol coincides with terminal state
            if b == '$' and j == (len(charList) - 1):
                print("Good input")
                exit()
            else:
                # verifies the next input symbol in the next state
                return verify(states[b], j + 1)
    print("Bad input")

word = input("Write the word:");
charList = list(word)
# always starts with non-terminal start S
verify(states['S'], 0)

