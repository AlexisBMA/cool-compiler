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
    walker.walk(gencode, tree)
    walker.walk(dataGen, tree)


    with open('test.asm', "w") as writer:
        writer.write(gencode.r)
        writer.write(dataGen.r)

if __name__ == '__main__':
    main()