default: test

test:
	py.test
	python setup.py check -r -s

clean:
	rm -f README.rst.html
	rm -f dist/*

release: test clean
	bumpversion patch && git log -1 -p
	python setup.py sdist bdist_wheel
	@echo
	@echo Upload to PyPI
	@echo python -m twine upload dist/*
