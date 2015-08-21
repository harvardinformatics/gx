"""
Created on Jul 16, 2015
Copyright (c) 2014
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller
"""
from gx.transformer import BaseTransformer

class CopyTransformer(BaseTransformer):
    '''
    Simply copies a segment directly
    '''

    def processSegment(self,segment,annotationreader,gwriter):
        '''
        Process a segment 
        '''
        segmentcopy = segment.copy()
        gwriter.addSegments([segmentcopy])
        
    @classmethod
    def getParameterDefs(self):
        return [
            {
                'name'      : 'GX_COPY_VERBOSE',
                'switches'  : ['--copy-verbose'],
                'required'  : False,
                'help'      : 'Increase verbosity for the copy transformer. Values should be yes or no',
                'default'   : 'no',
             }
        ]
        
        