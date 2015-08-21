"""
Created on Jul 14, 2015
Copyright (c) 2014
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller
"""

class ForkDispatcher(object):
    '''
    Uses forked children to dispatch segment data to transformers
    '''
    

    def __init__(self,**kwargs):
        '''
        Not sure if I need anything here
        '''
        self.n = kwargs['number-of-tasks']
        
    
    def dispatch(self,segment,transformer,annotationreader,genomewriter):
        pass

