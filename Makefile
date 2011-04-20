GCC=gcc

PLUGIN_SOURCE_FILES= \
  gcc-python.c \
  gcc-python-closure.c \
  optpass.c \
  tree.c

PLUGIN_OBJECT_FILES= $(patsubst %.c,%.o,$(PLUGIN_SOURCE_FILES))
GCCPLUGINS_DIR:= $(shell $(GCC) --print-file-name=plugin)

PYTHON_CONFIG=python-debug-config
PYTHON_CFLAGS=$(shell $(PYTHON_CONFIG) --cflags)
PYTHON_LDFLAGS=$(shell $(PYTHON_CONFIG) --ldflags)

CFLAGS+= -I$(GCCPLUGINS_DIR)/include -fPIC -O2 -Wall -Werror -g $(PYTHON_CFLAGS) $(PYTHON_LDFLAGS)

plugin: python.so

python.so: $(PLUGIN_OBJECT_FILES)
	$(GCC) $(CFLAGS) -shared $^ -o $@

clean:
	rm -f *.so *.o
	rm -f optpass.c

optpass.c: optpass.pyx
	cython $^ -o $@

tree.c: tree.pyx
	cython $^ -o $@

tree.pyx: tree.pyx.in tree-types.pyx.in
	cpp $(CFLAGS) tree.pyx.in -o $@

tree-types.txt: tree-types.txt.in
	cpp $(CFLAGS) $^ -o $@

tree-types.pyx.in: tree-types.txt maketreetypes.py
	python maketreetypes.py > tree-types.pyx.in

# Hint for debugging: add -v to the gcc options 
# to get a command line for invoking individual subprocesses
# Doing so seems to require that paths be absolute, rather than relative
# to this directory
TEST_CFLAGS= \
  -fplugin=$(shell pwd)/python.so \
  -fplugin-arg-python-script=test.py

test: plugin
	gcc -v $(TEST_CFLAGS) $(shell pwd)/test.c 
