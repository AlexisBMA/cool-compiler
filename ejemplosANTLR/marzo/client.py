from antlr4 import *
from antlr.marzoParser import marzoParser
from antlr.marzoLexer import marzoLexer
from listeners.datasegment import DataGenerator
from listeners.gencode import GenCode

import sys


def main():
    parser = marzoParser(CommonTokenStream(marzoLexer(FileStream("input.txt"))))
    tree = parser.program()

    gencode = GenCode()
    dataGen = DataGenerator()

    walker = ParseTreeWalker()
    
    # Por las constantes, ahora dataGen debe ir ANTES
    walker.walk(dataGen, tree)
    walker.walk(gencode, tree)

    with open('test.asm', "w") as writer:
        writer.write(dataGen.r)
        writer.write(gencode.r)
        

if __name__ == '__main__':
    main()