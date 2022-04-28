from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import * 
from util.structure import _allClasses as classDict

prohibitedClassnames = {'Int': badredefineint}
prohibitedInheritance = {'Bool': inheritsbool, 'String': inheritsstring, 'SELF_TYPE': inheritsselftype}
class semanticListener(coolListener):

    def __init__(self):
        self.main = False

    def enterKlass(self, ctx:coolParser.KlassContext):
        className = ctx.TYPE(0).getText()

        if className in prohibitedClassnames:
            raise prohibitedClassnames[className]()
        
        if ctx.TYPE(1):
            classInherits = ctx.TYPE(1).getText()
            if classInherits in prohibitedInheritance:
                raise prohibitedInheritance[classInherits]()
        
        if ctx.feature():
            feature = ctx.feature()
        
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True


    def enterFeature(self, ctx: coolParser.FeatureContext):
        featureID = ctx.ID().getText()
        if featureID == 'self' or featureID == 'SELF_TYPE':
            raise anattributenamedself("Feature ID not valid (self)")



    def exitKlass(self, ctx:coolParser.KlassContext):
        if (not self.main):
            raise nomain()

    
