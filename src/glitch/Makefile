glitch: glitch.cpp
	g++ -g -o glitch glitch.cpp `Wand-config --cflags --cppflags --ldflags --libs`

all: glitch

install: glitch
	cp glitch /usr/bin/glitch
