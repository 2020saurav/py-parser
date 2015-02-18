def foo(a):
	print a

def main():
	a = 42
	foo(a)
	#comment to be ignored by the lexer

if __name__=='__main__':
	main()