# A model based agent used to make sure that each 
# bank account has a sufficient minimum balance


import sys
lines=[]
intline=[]
minBalance = 1000
model={'A':0,'B':0}
with open(sys.argv[2]) as f:
#with open('modelbased.txt') as f:
    lines.extend(f.read().splitlines())
def modelbased(location,balance):
	model[location]=balance
	if int(model['A'])>=minBalance and int(model['B'])>=minBalance:
		return 'NoOp'
	elif int(balance) < minBalance:
		return 'Deposit money in'+' '+location 
	elif location == 'A':
		return 'Check bank B' 
	elif location == 'B':
		return 'Check bank A'
fo= open("output.txt", "w")
for line in lines:
	splits=line.split(',')
	balance=splits[1]
	location=splits[0]
	action=modelbased(location,balance)
	fo.write(action)
	fo.write('\n')
fo.close()
