from antlr.marzoListener import marzoListener
from antlr.marzoParser import marzoParser

import asm

class DataGenerator(marzoListener):
    def __init__(self):
        self.r = ''

    def enterProgram(self, ctx: marzoParser.ProgramContext):
        self.r += asm.tpl_start_data

    def enterDeclaracion(self, ctx: marzoParser.DeclaracionContext):
        self.r += asm.tpl_var_decl.substitute(
            varname = ctx.getChild(1).getText()
            )