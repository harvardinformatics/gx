"""
Created on Jul 14, 2015
Copyright (c) 2014
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller
"""

class SerialDispatcher(object):
    
    def __init__(self,GX_CONFIG):
        self.GX_CONFIG = GX_CONFIG
    '''
    Simple dispatcher that passes one segment at a time to the transformer
    '''
    def dispatch(self,segment,transformer,annotationreader,genomewriter):
        transformer.processSegment(segment,annotationreader,genomewriter)
        
        
    def finalize(self,transformer,annotreader,gwriter):
        '''
        Call write on the file
        '''
        gwriter.write()