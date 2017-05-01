all: main
	g++ main.o -shared -o main.so

main:
	g++ -c -fPIC -std=c++11 main.cpp -o main.o

clean:
	rm *.o
