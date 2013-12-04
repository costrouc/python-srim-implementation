example:
	echo "Running on 3 cores"
	mpirun -n 3 python pysrim.py --numIons=15 --ionEnergy=100000 --elementIon=Se -o example.csv
	echo "Output is file example.csv"
	echo "Run: disctibution.py example.csv example.png to create plot"
clean:
	rm -f *.pyc *~ temp.csv temp.png
test:
	echo "Test takes 30 minutes..."
	python timing.py
plot:
	mpirun -n 4 python pysrim.py -o --numIons=10 temp.csv
	python distribution.py temp.csv temp.png
	echo "plot is named temp.png"
	display temp.png

release: clean
	cd ..; tar -zcvf pysrim.tgz pysrim; mv pysrim.tgz pysrim/.
