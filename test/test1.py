def factorial(n):
	if(n<0):
		return 0
	elif(n<2):
		return 1
	else:
		return n*factorial(n-1)
print factorial(5)

for i in range(1,10):
	print factorial(i)
i = 10	
while(i>0):
	print factorial(i)
	i=i-1
else:
	print "Done"

