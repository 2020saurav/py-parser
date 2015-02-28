lineno = 1
def f():
	lineno=3
	for i in range(1,10):
		lineno+=1
		print lineno
f()
print lineno