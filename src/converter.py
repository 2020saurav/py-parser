import sys

def isAction(x):
	first = x[:x.find(":")]
	if first=="Action ":
		return True

def isReduce(x):
	third = x[x.find(":")+2:x.find(":")+3]
	if third == "R":
		return True
	else:
		return False

def getRule(x):
	rule = x[x.find("[")+1:x.find("]")]
	return rule

def left(x):
	return x[:x.find(" ")]

def right(x):
	children = x[x.find("->")+3:]
	children = children.split()
	return children

def getValue(x):
	value = x[x.find("with [")+6:x.find("] and")]
	value = value.split(",")
	return value

if __name__=="__main__":
	lines = open('dump').readlines()
	lines = [line for line in lines if isAction(line)]
	lines = reversed(lines)
	stack = [] # actually a list
	nodeId = 0
	sys.stdout = open('dot.dot','w')
	stack.append(("program",0,None))
	print "digraph G \n{\n"
	print "\tnode0 [label=\"program\"];"
	for line in lines:
		if isReduce(line):
			item = stack.pop()
			rule = getRule(line)
			children = right(rule)
			i=0
			value = getValue(line)
			for child in children:
				nodeId+=1
				stack.append((child,nodeId,item[2]))
				if(value[i]!="None"):
					print "\tnode"+str(nodeId)+" [label= \""+child+"\\n"+value[i]+"\"];"
				else:
					print "\tnode"+str(nodeId)+" [label= \""+child+"\"];"

				print "\tnode"+str(item[1])+" -> node"+str(nodeId)+";"
				i+=1
		else:
			stack.pop()
			pass
	print "}"
