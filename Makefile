CXX=g++
CPPFLAGS=-std=c++14 -O2 -Wall
LINK_OPTS=-shared -Wl,--export-dynamic
COMPILE_OPTS=-fPIC
INCLUDES=-I /usr/include/python3.5/
LIBS=-L /usr/lib/x86_64-linux-gnu/ -l boost_python-py35 -l boost_graph

%.so: %.o
	$(CXX) $^ $(CPPFLAGS) $(LINK_OPTS) $(LIBS) -o $@

%.o: %.cpp
	$(CXX) $(CPPFLAGS) $(COMPILE_OPTS) $(INCLUDES)  -c $<

.PHONY: clean

clean:
	rm -f *.o *.so *~ core
