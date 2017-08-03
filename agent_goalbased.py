# A goal based agent used to make sure that each 
# bank account has a sufficient minimum balance


import sys
lines=[]
intline=[]
minBalance = 1000
model={'A':0,'B':0}
with open(sys.argv[2]) as f:
#with open('goalbased.txt') as f:
    lines.extend(f.read().splitlines())
def goalbased(location,balance):
	model[location]=balance
	if int(model['A'])>=minBalance and int(model['B'])>=minBalance:
		return 'Stop'
	elif int(balance) < minBalance:
		return 'Deposit money in'+' '+location
	elif location == 'A':
		return 'Check Bank-B' 
	elif location == 'B':
		return 'Check Bank-A'
fo= open("output.txt", "w")
for line in lines:
	splits=line.split(',')
	balance=splits[1]
	location=splits[0]
	action=goalbased(location,balance)
	if action == 'Stop':
		fo.write(str(action))
		fo.write('\n')
		break
	fo.write(action)
	fo.write('\n')
fo.close()
