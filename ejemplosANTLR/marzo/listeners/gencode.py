from antlr.marzoListener import marzoListener
from antlr.marzoParser import marzoParser

import asm

class GenCode(marzoListener):
    def __init__(self):
        self.result = ''
        self.stack = []
        self.labels = 0
    
    def enterProgram(self, ctx:marzoParser.ProgramContext):
        self.result += asm.tpl_start_text
    
    def exitProgram(self, ctx: marzoParser.ProgramContext):
        for c in ctx.getChildren():
            self.result += c.code
        self.result += asm.tpl_end

    def exitPrimaria(self, ctx:marzoParser.PrimariaContext):
        self.stack.append(
            asm.tpl_immediate.substitute(immediate=ctx.getText())
            )

    def exitPrimaria_string(self, ctx: marzoParser.Primaria_stringContext):
        self.stack.append(
            asm.tpl_string_const.substitute(
                name = ctx.label
            )
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
        ctx.code = asm.tpl_asignacion.substitute(
             prev = self.stack.pop(),
             name = ctx.getChild(0).getText()
        )
    
    def exitVar(self, ctx: marzoParser.VarContext):
        self.stack.append(
            asm.tpl_var.substitute(name=ctx.getText())
        )
    
    def exitPrintint(self, ctx: marzoParser.PrintintContext):
        ctx.code = asm.tpl_print_int.substitute(
            prev=self.stack.pop()
        )

    def exitPrintstr(self, ctx: marzoParser.PrintstrContext):
        ctx.code = asm.tpl_print_str.substitute(
            prev=self.stack.pop()
        )

    def exitIf(self, ctx: marzoParser.IfContext):
        self.labels = self.labels = self.labels + 1
        ctx.code = asm.tpl_if.substitute(
            prev = self.stack.pop(),
            n = self.labels, 
            stmt_true = ctx.statement(0).code
        )

    def exitIfelse(self, ctx: marzoParser.IfelseContext):
        self.labels = self.labels = self.labels + 1
        ctx.code = asm.tpl_if_else.substitute(
            prev = self.stack.pop(),
            n = self.labels, 
            stmt_true = ctx.statement(0).code, 
            stmt_false = ctx.statement(1).code
        )

    def exitBlock(self, ctx: marzoParser.BlockContext):
        ctx.code = ''
        for c in ctx.statement():
            ctx.code += c.code
    
    def exitWhile(self, ctx: marzoParser.WhileContext):
        self.labels = self.labels + 1
        ctx.code = asm.tpl_while.substitute(
            test = self.stack.pop(),
            n = self.labels,
            stmt = ctx.statement().code
        )

    def exitProcedure(self, ctx: marzoParser.ProcedureContext):
        # No me importan las variables ヽ(°〇°)ﾉ
        ctx.code = asm.tpl_procedure.substitute(
            name = ctx.name.text,
            code = ctx.statement().code
        )

    def exitCall(self, ctx: marzoParser.CallContext):
        r = ''
        for c in ctx.expression():
            r += self.stack.pop()
            r += asm.tpl_push_arg
        
        self.stack.append(
            asm.tpl_call.substitute(
                push_arguments = r,
                name = ctx.Variable()
            )
        )
    
    def exitReturn(self, ctx: marzoParser.ReturnContext):
        ctx.code = self.stack.pop()