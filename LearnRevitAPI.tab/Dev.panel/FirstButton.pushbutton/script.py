# -*- coding: utf-8 -*-
__title__ = "Rename Views"
__doc__ = """Version = 1.0
Date    = 19.08.2025
_____________________________________________________________________
Description:
Rename Views in Revit by using Find/Replace Logic.
_____________________________________________________________________
How-to:
-> Click on the button
-> Select Views
-> Define Renaming Rules
-> Rename Views
_____________________________________________________________________
Last update:
- [19.08.2025] - 1.0 RELEASE
_____________________________________________________________________
Author: Nam Pham"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
#==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import revit, forms

# .NET Imports (You often need List import)
import clr
clr.AddReference("System")
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
#==================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
#==================================================

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
#==================================================
# 1️⃣ Select Views

sel_id = uidoc.Selection.GetElementIds()
sel_element = [doc.GetElement(e_id) for e_id in sel_id]
sel_view = [e for e in sel_element if issubclass(type(e), View)]

# If None Selected - Promt SelectViews from pyrevit.forms.select_views()
if not sel_view:
    sel_view= forms.select_views()

#Ensure Views Selected
if not sel_view:
    forms.alert("No views selected. Please try again", exitscript=True)

#2️⃣🅰️ Define Renaming Rules

#prefix  = 'pre - '
#find    = 'Level'
#replace = 'FloorPlan'
#suffix  = ' - suf'

#2️⃣🅱️ Define Renaming Rules (UI FORM)
#https://revitpythonwrapper.readthedocs.io/en/latest/ui/forms.html#flexform

from rpw.ui.forms import (FlexForm, Label, TextBox, Separator, Button, CheckBox)
components =    [Label('Prefix:'), TextBox ('prefix'),
                Label('Find:'), TextBox ('find'),
                Label('Replace:'), TextBox ('replace'),
                Label('Suffix:'), TextBox ('suffix'),
                Separator(),           Button('Renaming Views')]

form = FlexForm('Rename Views', components)
form.show()

user_inputs = form.values
prefix  = user_inputs['prefix']
find  = user_inputs['find']
replace    = user_inputs['replace']
suffix = user_inputs['suffix']

# 🔒 Start Transaction to make changes in project
t = Transaction(doc, 'Rename Views')

t.Start()   #🔓

# 3️⃣Create new View Name
for view in sel_view:
    old_name = view.Name
    new_name = prefix + old_name.replace(find, replace) + suffix

    #4️⃣ Ensure Views (Ensure unique View Name)
    for i in range(20):
        try:
            view.Name = new_name #✅This actually renames the views
            print('{} -> {}'.format(old_name, new_name))
            break
        except:
            new_name += '*'

t.Commit()  #🔒

print('-'*50)
print('Done!')