from antlr.marzoListener import marzoListener
from antlr.marzoParser import marzoParser

import asm

class GenCode(marzoListener):
    def __init__(self):
        self.r = ''
        self.stack = []
    
    def enterProgram(self, ctx:marzoParser.ProgramContext):
        self.r += asm.tpl_start_text
    
    def exitProgram(self, ctx: marzoParser.ProgramContext):
        self.r += asm.tpl_end

    def exitPrimaria(self, ctx:marzoParser.PrimariaContext):
        self.stack.append(
            asm.tpl_immediate.substitute(immediate=ctx.getText())
            )

    def exitSuma(self, ctx:marzoParser.SumaContext):
        self.stack.append(
            asm.tpl_suma.substitute(
                right=self.stack.pop(), 
                left=self.stack.pop()
                )
            )

    def exitResta(self, ctx: marzoParser.RestaContext):
        self.stack.append(
            asm.tpl_resta.substitute(
                right=self.stack.pop(), 
                left=self.stack.pop()
                )
            )
    def exitAsignacion(self, ctx: marzoParser.AsignacionContext):
        self.r += asm.tpl_asignacion.substitute(
             prev=self.stack.pop(),
             name = ctx.getChild(0).getText()
        )
    
    def exitVar(self, ctx: marzoParser.VarContext):
        self.stack.append(
            asm.tpl_var.substitute(name=ctx.getText())
        )
    
    def exitPrintint(self, ctx: marzoParser.PrintintContext):
        self.r += asm.tpl_print_int.substitute(
            prev=self.stack.pop()
        )
