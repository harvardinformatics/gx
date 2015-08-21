'''
Created on Jul 17, 2015
Copyright (c) 2015
Harvard Informatics and Scientific Applications
All rights reserved.

@author: Aaron Kitzmiller
'''

__all__ = []

import pkgutil
import inspect

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue

        globals()[name] = value
        __all__.append(name)
        
