# -*- coding: utf-8 -*-

#import
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

import clr
clr.AddReference("System")
from System.Collections.Generic import List

# VARIABLES
#==================================================

doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

#MAIN
#==================================================

# Reusable Snippets

def get_selected_elements(filter_types = None):
    """Get selected Elements in Revit UI.
    You can provide a list of types for filter_types parameter (optional).

    e.d.
    sel_walls = get_selected_elements([Wall])
    """
    selected_elements_ids = uidoc.Selection.GetElementIds()
    selected_elements = [doc.GetElement(e_id) for e_id in selected_elements_ids]

    #Filter Selection (Optionally)
    if filter_types:
        return [el for el in selected_elements if type(el) in filter_types]
    return selected_elements