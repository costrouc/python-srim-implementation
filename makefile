clean:
	rm -f *.pyc *~ temp.csv
test:
	echo "Test takes 30 minutes..."
	python timing.py
release: clean
	cd ..; tar -zcvf pysrim.tgz pysrim; mv pysrim.tgz pysrim/.
