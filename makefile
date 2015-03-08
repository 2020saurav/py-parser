parser: src/*
	cp src/* bin/
	python -m py_compile bin/*.py
	mv bin/parser.py bin/parser
	chmod +x bin/parser

clean:
	rm -f -rf bin/*
	rm -f *.dot
	rm -f *.png
	rm -f parse*
	rm -f dump