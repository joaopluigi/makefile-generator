#!/usr/bin/env python

#################################################################
#                                                               #
#                      Makefile Generator                       #
#          Simple and easy makefile generator made in Python!   #
#                                                               #
#    Usage:                                                     #
#       - set execution permission                              #
#       - run makefile_generator.py                             #
#       - make                                                  #
#       - binary file named 'program' will be created at ./bin/ #
#                                                               #
#   !Important!                                                 #
#       - .c files must be on ./src/                            #
#       - .h files must be on ./inc/                            #
#       - libs must be on ./lib/                                #
#                                                               #
################################################################

import os
from fnmatch import fnmatch

pattern = "*.c"
directory = 'src/'

## bin dir
if not os.path.exists('bin/'):
    os.makedirs('bin/')

## obj dir
if not os.path.exists('obj/'):
    os.makedirs('obj/')

# write to makefile
with open('makefile', 'w') as makefile:

    # Compiler
    makefile.write('CC = gcc\n\n')

    # DIRs
    makefile.write('BDIR = bin\n')
    makefile.write('IDIR = inc\n')
    makefile.write('ODIR = obj\n')
    makefile.write('LDIR = lib\n\n')

    # Libs & Flags
    makefile.write('LIBS = -lm\n')
    makefile.write('CFLAGS = -I$(IDIR)\n\n')

    # Headers
    makefile.write('_DEPS = $(*.h)\n')
    makefile.write('DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))\n\n')

    # OBJs (from sources)
    makefile.write('_OBJ = ')

    # Get all source files from src/
    for path, subdirs, files in os.walk(directory):
        for name in files:
            if fnmatch(name, pattern):
                objdir = path.replace("src/", "obj/")
                makefile.write((os.path.join(path, name).replace(".c", ".o").replace("src/", "")) + ' ')
    
    # Set OBJ dest dir
    makefile.write('\nOBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))\n\n')

    # Project compilation
    makefile.write('$(ODIR)/%.o: src/%.c $(DEPS)\n')
    makefile.write('\t\t\t $(CC) -c -o $@ $< $(CFLAGS)\n\n')

    # Make algorithm
    makefile.write('default: $(BDIR)/program\n\n')
    makefile.write('$(BDIR)/program: $(OBJ)\n')
    makefile.write('\t\t\t $(CC) -o $@ $^ $(CFLAGS) $(LIBS)\n\n')

    # PHONY
    makefile.write('.PHONY: clean\n\n')

    # Clean
    makefile.write('clean:\n')
    makefile.write('\t\t\t rm -rf $(BDIR)/program\n')

