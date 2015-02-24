import sys
def factorial (num):
	if(num<20):
		return 21
	else:
		return num*factorial(num-1)

for index in range(10,25):
	print factorial(index)

print "Hello"
