from antlr.marzoListener import marzoListener
from antlr.marzoParser import marzoParser

import asm

class DataGenerator(marzoListener):
    def __init__(self):
        self.r = ''
        self.constants = 0

    def enterProgram(self, ctx: marzoParser.ProgramContext):
        self.r += asm.tpl_start_data

    def enterDeclaracion(self, ctx: marzoParser.DeclaracionContext):
        self.r += asm.tpl_var_decl.substitute(
            varname = ctx.getChild(1).getText()
        )
        ctx.code = ''

    def enterPrimaria_string(self, ctx: marzoParser.Primaria_stringContext):
        self.constants = self.constants + 1
        ctx.label = "var{}".format(self.constants)
        self.r += asm.tpl_string_const_decl.substitute(
            name = ctx.label, content = ctx.getText()
        )
