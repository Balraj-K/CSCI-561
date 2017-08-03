# A reflex based agent used to make sure that each 
# bank account has a sufficient minimum balance


import sys
lines=[]
intline=[]
minBalance = 1000
with open(sys.argv[2]) as f:
#with open('simplereflex.txt') as f:
    lines.extend(f.read().splitlines())
def reflex(location,balance):
	if int(balance) <= minBalance:
		return 'Deposit money in '+' '+location 
	elif location == 'A':
		return 'Check Bank-B' 
	elif location == 'B':
		return 'Check Bank-A'
fo= open("output.txt", "w")
for line in lines:
	splits=line.split(',')
	balance=splits[1]
	location=splits[0]
	action=reflex(location,balance)
	fo.write(action)
	fo.write('\n')
fo.close()
