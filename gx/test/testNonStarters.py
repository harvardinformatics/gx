"""
Created on Jul 14, 2015
Copyright (c) 2014
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller

Tests of failure conditions that prevent gx from starting
"""

import unittest


class Test(unittest.TestCase):


    def setUp(self):
        # A set of good parameters that are substituted for bad ones
        self.parameters = {
            'GX_GENOME_READER'         : 'PyFastaGenomeReader',
            'GX_SEGMENT_DISPATCHER'    : 'SerialDispatcher',
            'GX_TRANSFORMER'           : 'CopyTransformer',
            'GX_GENOME_WRITER'         : 'BufferedFastaWriter',
        }
            


    def tearDown(self):
        pass

    def testHappy(self):
        '''
        These should work
        '''
        pass
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFailures']
    unittest.main()