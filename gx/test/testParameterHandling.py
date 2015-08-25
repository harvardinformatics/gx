"""
Created on Jul 14, 2015
Copyright (c) 2014
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller

Tests of failure conditions that prevent gx from starting
"""
import os,sys,subprocess
import unittest

from hex.cmd import Command

def getOutput(cmd):
    '''
    Return the returncode, stdout, stderr for the given command 
    '''
    p = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = p.communicate()
    return [p.returncode,stdout.strip(),stderr.strip()]
    
class Test(unittest.TestCase):


    def setUp(self):
        # A set of good parameters that are substituted for bad ones
        # Existing environment is stored and cleared here, then 
        # reset in tearDown
        self.parameterkeys = [
            'GX_GENOME_READER',
            'GX_SEGMENT_DISPATCHER',
            'GX_TRANSFORMER',
            'GX_GENOME_WRITER',
        ]
         
        self.oldvalues = {}
        for key in self.parameterkeys:
            if os.environ.get(key,None) is not None:
                self.oldvalues[key] = os.environ[key]
                del os.environ[key]       
             
 
 
    def tearDown(self):
        # Reset the original environment
        for key in self.parameterkeys:
            if key in self.oldvalues:
                os.environ[key] = self.oldvalues[key]
            

    def testParametersWithCleanEnvironment(self):
        '''
        Test parameter gathering.  Make sure defaults are set when env is clean.
        '''
        c = Command('gxf.py --help')
        [returncode,stdout,stderr] = c.run()
        
        for defaultclass in ['PyfastaReader','BufferedFastaWriter','SerialDispatcher']:           
            self.assertTrue("%s]" % defaultclass in stdout.replace("\n",""),"Can't find %s in %s" % (defaultclass,stdout.replace("\n","")))
        
        # Make sure the copy transformer item got picked up
        self.assertTrue("--copy-verbose GX_COPY_VERBOSE" in stdout)
        
        # Make sure the other basics are there
        basics = [
            "-i GX_INPUT_GENOME_FILE, --input-file GX_INPUT_GENOME_FILE",
            "-s GX_SEGMENT_SIZE, --segment-size GX_SEGMENT_SIZE",
            "-x GX_TRANSFORMER, --genome-transformer GX_TRANSFORMER",
            "-o GX_OUTPUT_GENOME_FILE, --output-file GX_OUTPUT_GENOME_FILE"
        ]
        for teststr in basics:
            self.assertTrue(teststr in stdout, "Can't find %s in %s" % (str,stdout))
            
            
        
    def testEnvSetting(self):
        '''
        Setting env vars should show up as new default in the help message
        '''
        testparameters = {
            'GX_GENOME_READER'          : 'testreader',
            'GX_SEGMENT_DISPATCHER'     : 'testdispatcher',
            'GX_TRANSFORMER'            : 'testtransformer',
            'GX_GENOME_WRITER'          : 'testwriter',            
        }
        for key, value in testparameters.iteritems():
            os.environ[key] = value

        c = Command('gxf.py --help')
        [returncode,stdout,stderr] = c.run()
        
        for key,value in testparameters.iteritems():
            self.assertTrue("%s]" % value in stdout.replace("\n",""), "Can't find %s in %s" % (value,stdout.replace("\n","")))
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFailures']
    unittest.main()