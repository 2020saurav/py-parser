import sys
def factorial(n):
	if(n<2):
		return 1
	else:
		return n*factorial(n-1)

for i in range(1,10):
	print factorial(i)


