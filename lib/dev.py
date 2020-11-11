import bpy
import os, sys
import importlib
sys.path.extend([os.path.join('.', 'lib')])
LIB_HOME='/Users/photon/DevOps/Projects/Solar_System_Model' 
os.chdir(LIB_HOME)
import data
from planet import Planet 
import moon 
from moon import Moon
import blender 
import orbital
import importlib 

def bpy_add_driver_namespace(func):
    bpy.app.driver_namespace[func] = getattr()

def import_bpy_functions(funcs):
    for func in funcs:
        print(f"importing function: {func}")    
        bpy.app.driver_namespace[func] = getattr(blender, func)

import_bpy_functions(blender.HELPERS)