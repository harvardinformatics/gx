'''
Created on Jun 24, 2015
Copyright (c) 2015
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller

Base classes for the gx genome transformer
'''

def getClassFromName(classname):
    """
    Utility that will return the class object for a fully qualified 
    classname
    """
    try:
        parts = classname.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)            
        return m
    except ImportError:
        print "Unable to import %s" % classname
    return None


class Segment(object):
    '''
    This is the segment of genome that is passed to the Transformer.  Also they 
    can be created to compose the new genome.
    '''
    def __init__(self,start,end,sequence,chr):
        self.start = start
        self.end = end
        self.sequence = sequence
        self.chr = chr

    def copy(self):
        '''
        Return a copy of this Segment
        '''
        copyseg = Segment(self.start,self.end,self.sequence,self.chr)
        return copyseg
        
    def insertSegment(self,Segment,start):
        '''
        Insert a segment into this segment
        '''
        pass
    
    def appendSegment(self,Segment):
        '''
        Append Segment to this segment
        '''
        pass
    
    def getString(self,start=None,end=None):
        '''
        Nucleotide base string for this segment
        '''
        pass
    
    def getAnnotations(self):
        '''
        Get all the annotations that overlap with this segment
        '''
        pass
    
    def locations(self):
        '''
        Return an iterator over the locations
        '''
        pass
    


class Genome(object):
    '''
    This is some meta data, along with some functions for manipulating segments
    '''
    def __init__(self,name,genomeloader,annotationloader):
        self.genomeloader = genomeloader
        self.annotationloader = annotationloader
    
    def appendSegment(self,Segment):
        '''
        Adds a segment to the end of this Genome
        '''
        pass
    
    
    def insertSegment(self,Segment,start):
        '''
        Inserts a segment at the given location
        '''
        pass
    
    def segments(self):
        '''
        Get a segment iterator
        '''
        pass
        
class GenomeLoader(object):
    '''
    Base class for things that load genomes.  One may read the whole thing up
    into a string, another may read chunks on demand, another may use numpy
    arrays
    '''
    pass

class GenomeWriter(object):
    '''
    Could write to one concatenated FASTA for each contig.  Or could 
    generate separate files for each chromosome.
    '''
    pass
    
    
class Transformer(object):
    '''
    Base class for code that transforms genomes from one form to 
    another
    '''
    
    def processSegment(self,segment):
        pass
        