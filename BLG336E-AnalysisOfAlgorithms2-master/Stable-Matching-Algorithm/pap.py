men = {}		#men dictionary, "name":"partner name"
women = {}		#women dictionary, "name":"partner name"
pMen = {}		#list of men preferences, "name": [preferences]
pWomen = {}		#list of women preferences, "name": [preferences]

n = int(raw_input("Number of total people (man + woman): "))

for i in xrange(n//2):
	pref = []
	name = raw_input("Name of " + str(i+1) + " th man: ")
	for x in xrange(1,n//2 + 1):
		pref += raw_input( str(x) + "th pref of " + name + ": " )
	pMen[name] = pref
	men[name] = ""

for i in xrange(n//2):
	pref = []
	name = raw_input("Name of " + str(i+1) + " th woman: ")
	for x in xrange(1,n//2 + 1):
		pref += raw_input( str(x) + "th pref of " + name + ": " )
	pWomen[name] = pref
	women[name] = ""

# eslesmemis erkegi bulmak icin
def searchForEmpty( fMen ):
	for i in fMen:
		if fMen[i] == "":
			return True
	return False

# erkegin tercihleri arasinda eslesmemis ilk kisiyi bulmak icin
def searchFirstWoman( man, i ):
    return pMen[man][i]

# search for given name's index
def searchIndex( people, name ):
    for i in xrange(len(people)):
        if[people[i] == name]:
            return i

while searchForEmpty( men ):
    man = ""
    for i in men.keys():
        if men[i] == "":
            man = i
            break

    ctr = 0
    while ctr < (n//2):
        woman = searchFirstWoman(man, ctr)
        if women[woman] == "":
            women[woman] = man
            men[man] = woman
            break
        else:
            manIndex  = searchIndex(pWomen.keys(), man)
            partIndex = searchIndex(pWomen.keys(), women[woman])
            if manIndex < partIndex:
                men[women[woman]] = ""
                women[woman] = pWomen[woman][manIndex]
                men[pWomen[woman][manIndex]] = woman
            else:
                ctr += 1


print men
print women
