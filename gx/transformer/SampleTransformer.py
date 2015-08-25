"""
Created on Jul 16, 2015
Copyright (c) 2014
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller
"""
from collections import OrderedDict
from random import randint

from gx.transformer import BaseTransformer

class SampleTransformer(BaseTransformer):
    '''
    Picks a segment randomly from each chromosome
    '''
    @classmethod
    def getParameterDefs(self):
        return None
    
    def __init__(self,GX_CONFIG):
        self.segments = OrderedDict()

    def processSegment(self,segment,annotationreader,gwriter):
        '''
        Collect the segments into a list 
        '''
        if segment.chr not in self.segments:
            self.segments[segment.chr] = []
            
        self.segments[segment.chr].append(segment)
        
    def finalize(self,gwriter,annotationreader):
        '''
        Randomly pick a single segment from the list for each chr
        '''
        for chr in self.segments.keys():
            index = randint(0,len(self.segments[chr]) - 1)
            gwriter.addSegments([self.segments[chr][index]])
            
        gwriter.write()
        
        
        
        