"""
Created on Jul 14, 2015
Copyright (c) 2014
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller

Tests of failure conditions that prevent gx from starting
"""

import unittest
from hex.cmd import Command

class Test(unittest.TestCase):


    def setUp(self):
        # A set of good parameters that are substituted for bad ones
        self.parameters = {
            'GX_GENOME_READER'         : 'PyfastaReader',
            'GX_SEGMENT_DISPATCHER'    : 'SerialDispatcher',
            'GX_TRANSFORMER'           : 'CopyTransformer',
            'GX_GENOME_WRITER'         : 'BufferedFastaWriter',
        }
            
    def tearDown(self):
        pass

    def testBadRequiredInputs(self):
        '''
        Test common inputs (genome reader, segment dispatcher, transformer, genome writer, annotation reader) using bad values.
        Both fully specified and bare class names are tested.
        '''
        badclasses = {
            'GX_GENOME_READER'      : 'gx.io.badclass',
            'GX_SEGMENT_DISPATCHER' : 'gx.dispatcher.badclass',
            'GX_TRANSFORMER'        : 'gx.transformer.badclass',
            'GX_GENOME_WRITER'      : 'gx.io.badclass',
        }
        for key in self.parameters.keys():            
            params = self.parameters.copy()
            params[key] = 'badclass'
            params['GX_INPUT_GENOME_FILE'] = 'ce10sample.fa'
            params['GX_OUTPUT_GENOME_FILE'] = 'out.fa'
            params['GX_SEGMENT_SIZE'] = 100
            cmd = Command('gxf.py --genome-reader {GX_GENOME_READER} --genome-writer {GX_GENOME_WRITER} --segment-dispatcher {GX_SEGMENT_DISPATCHER} --genome-transformer {GX_TRANSFORMER} -i {GX_INPUT_GENOME_FILE} -o {GX_OUTPUT_GENOME_FILE} -s {GX_SEGMENT_SIZE}'.format(**params))
            [returncode,stdout,stderr] = cmd.run()
            self.assertTrue(returncode != 0,"gxf.py succeeded?")
            self.assertTrue('Error : Unable to import %s.' % badclasses[key] in stderr, "Error message is incorrect: %s" % stderr)
            
        badclasses = {
            'GX_GENOME_READER'      : 'my.bad.classes.badclass',
            'GX_SEGMENT_DISPATCHER' : 'my.bad.classes.badclass',
            'GX_TRANSFORMER'        : 'bad.badclass',
            'GX_GENOME_WRITER'      : 'super.badclass',
        }
        for key in self.parameters.keys():            
            params = self.parameters.copy()
            params[key] = badclasses[key]
            params['GX_INPUT_GENOME_FILE'] = 'ce10sample.fa'
            params['GX_OUTPUT_GENOME_FILE'] = 'out.fa'
            params['GX_SEGMENT_SIZE'] = 100
            cmd = Command('gxf.py --genome-reader {GX_GENOME_READER} --genome-writer {GX_GENOME_WRITER} --segment-dispatcher {GX_SEGMENT_DISPATCHER} --genome-transformer {GX_TRANSFORMER} -i {GX_INPUT_GENOME_FILE} -o {GX_OUTPUT_GENOME_FILE} -s {GX_SEGMENT_SIZE}'.format(**params))
            [returncode,stdout,stderr] = cmd.run()
            self.assertTrue(returncode != 0,"gxf.py succeeded?")
            self.assertTrue('Error : Unable to import %s.' % badclasses[key] in stderr, "Error message is incorrect: %s" % stderr)
        
        
        # No input file
        params = self.parameters.copy()
        params['GX_OUTPUT_GENOME_FILE'] = 'out.fa'
        params['GX_SEGMENT_SIZE'] = 100
        cmd = Command('gxf.py --genome-reader {GX_GENOME_READER} --genome-writer {GX_GENOME_WRITER} --segment-dispatcher {GX_SEGMENT_DISPATCHER} --genome-transformer {GX_TRANSFORMER} -o {GX_OUTPUT_GENOME_FILE} -s {GX_SEGMENT_SIZE}'.format(**params))
        [returncode,stdout,stderr] = cmd.run()
        self.assertTrue(returncode != 0,"gxf.py succeeded?")
        self.assertTrue('Error : --input-file/GX_INPUT_GENOME_FILE must be defined' in stderr, "Error message is incorrect: %s" % stderr)
        
        # No segment size 
        params = self.parameters.copy()
        params['GX_OUTPUT_GENOME_FILE'] = 'out.fa'
        params['GX_INPUT_GENOME_FILE'] = 'ce10sample.fa'
        cmd = Command('gxf.py --genome-reader {GX_GENOME_READER} --genome-writer {GX_GENOME_WRITER} --segment-dispatcher {GX_SEGMENT_DISPATCHER} --genome-transformer {GX_TRANSFORMER} -i {GX_INPUT_GENOME_FILE} -o {GX_OUTPUT_GENOME_FILE}'.format(**params))
        [returncode,stdout,stderr] = cmd.run()
        self.assertTrue(returncode != 0,"gxf.py succeeded?")
        self.assertTrue('Error : --segment-size/GX_SEGMENT_SIZE must be defined' in stderr, "Error message is incorrect: %s" % stderr)
        
        # No output file
        params = self.parameters.copy()
        params['GX_INPUT_GENOME_FILE'] = 'ce10sample.fa'
        params['GX_SEGMENT_SIZE'] = 100
        cmd = Command('gxf.py --genome-reader {GX_GENOME_READER} --genome-writer {GX_GENOME_WRITER} --segment-dispatcher {GX_SEGMENT_DISPATCHER} --genome-transformer {GX_TRANSFORMER} -i {GX_INPUT_GENOME_FILE} -s {GX_SEGMENT_SIZE}'.format(**params))
        [returncode,stdout,stderr] = cmd.run()
        self.assertTrue(returncode != 0,"gxf.py succeeded?")
        self.assertTrue('Error : --output-file/GX_OUTPUT_GENOME_FILE must be defined' in stderr, "Error message is incorrect: %s" % stderr)
        
        
       

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFailures']
    unittest.main()