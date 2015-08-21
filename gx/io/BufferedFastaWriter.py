"""
Created on Jul 14, 2015
Copyright (c) 2014
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller
"""

class BufferedFastaWriter(object):
    '''
    Caches a set of segments, then appends them to the output file.  Characters between
    newlines are based on the column_number value. 
    '''


    def __init__(self,GX_CONFIG):
        '''
        Constructor
        '''
        self.segments = {}
        self.column_number = 80
        
        if 'GX_FASTA_COLUMN_NUMBER' in GX_CONFIG:
            try:
                self.column_number = int(GX_CONFIG['GX_FASTA_COLUMN_NUMBER'])
            except Exception:
                raise Exception('Value of GX_FASTA_COLUMN_NUMBER %s is not an integer' % str(GX_CONFIG['GX_FASTA_COLUMN_NUMBER']))
        
        
                # Check the output file
        if 'GX_OUTPUT_GENOME_FILE' not in GX_CONFIG.keys():
            raise Exception('Output genome file must be defined')
        
        
        # Test that the file is writable if verify-resources is set
        if 'GX_VERIFY_RESOURCES' in GX_CONFIG and GX_CONFIG['GX_VERIFY_RESOURCES']:
            pass
        

        self.output_file_name = GX_CONFIG['GX_OUTPUT_GENOME_FILE']
        
        
    def addSegments(self,segments):
        '''
        Add segments to the cache
        '''
        for seg in segments:
            
            if seg.chr not in self.segments:
                self.segments[seg.chr] = []
                
            self.segments[seg.chr].append(seg)
        
    def write(self):
        '''
        Actually writes the segments to the file
        '''
        
        f = open(self.output_file_name,'w')
        
        for chr in self.segments.keys():
            f.write(">%s\n" % chr)
            segs = self.segments[chr]
            seqstr = ''
            for seg in segs:
                seqstr += seg.sequence
                while len(seqstr) > self.column_number:
                    f.write("%s\n" % seqstr[:self.column_number])
                    seqstr = seqstr[self.column_number:]
        f.close()
        