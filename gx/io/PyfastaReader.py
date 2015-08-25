"""
Created on Jul 14, 2015
Copyright (c) 2014
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller
"""

import os

from pyfasta import Fasta

from gx import Segment

class PyfastaReader(object):
    '''
    Issues genome segments using the pyfasta reader
    '''

    def __init__(self,GX_CONFIG):
        '''
        Constructor
        Parameters:
            GX_INPUT_GENOME_FILE       The input fasta file name
            GX_SEGMENT_SIZE            Size of the segment being read
            GX_START_CHROMOSOME        First chromosome that should be read
            GX_START_LOCATION          Start location for fasta reading
        '''
        self.verbose = GX_CONFIG['GX_VERBOSE']
        self.start_chromosome = None
        self.start_location = 0
        
        # Check the input file
        if 'GX_INPUT_GENOME_FILE' not in GX_CONFIG.keys():
            raise Exception('Input genome file must be defined')
        
        if not os.path.isfile(GX_CONFIG['GX_INPUT_GENOME_FILE']):
            raise Exception('Input genome file %s does not exist' % GX_CONFIG['GX_INPUT_GENOME_FILE'])
            
        self.fasta = Fasta(GX_CONFIG['GX_INPUT_GENOME_FILE'])
        
        
        # Check the segment size       
        if 'GX_SEGMENT_SIZE' not in GX_CONFIG.keys():
            raise Exception('Segment size must be defined')
        
        try:
            self.segment_size = int(GX_CONFIG['GX_SEGMENT_SIZE'])
        except Exception, e:
            raise Exception('Segment size %s is not an integer' % str(GX_CONFIG['GX_SEGMENT_SIZE']))
        
        
        # Start location
        if 'GX_START_CHROMOSOME' in GX_CONFIG:
            self.start_chromosome = GX_CONFIG['GX_START_CHROMOSOME']
            
        if 'GX_START_LOCATION' in GX_CONFIG:
            try:
                self.start_location = int(GX_CONFIG['GX_START_LOCATION'])
            except Exception:
                raise Exception('Start location is not an integer')
        
        # End location
    
    def segments(self):
        '''
        Generator for Segments
        '''
        startchr = self.start_chromosome
        start = self.start_location
        chrs = [x[0] for x in sorted(self.fasta.index.items(), key=lambda a: a[1][0])]
        for chr in chrs:
            segcount = 0
            if self.verbose:
                print "Reading chr %s" % chr
            # Skip forward if a starting chr was defined
            if startchr is not None and startchr != chr:
                continue
            else:
                startchr = None
                
            for kmer in Fasta.as_kmers(self.fasta[chr],self.segment_size):
                end = start + self.segment_size                
                seg = Segment(start, end, kmer[1] ,chr)
                segcount += 1
                if self.verbose and segcount % 1000 == 0:
                    print "Read %d segments" % segcount
                yield seg
                start = end
        