"""
Created on Jul 17, 2015
Copyright (c) 2014
Harvard FAS Research Computing
All rights reserved.

@author: Aaron Kitzmiller
"""


class BaseTransformer(object):
    '''
    Base class for Transformers
    '''
    
    def __init__(self,GX_CONFIG):
        self.GX_CONFIG = GX_CONFIG

    def processSegment(self,segment,annotationreader,gwriter):
        raise Exception("processSegment must be implemented")
    
    @classmethod
    def getParameterDefs(cls):
        '''
        Return the parameter defs for this transformer so that the argument parser can ask for them.
        
        An array of dicts should be returned.  The keys can be any of the python ArgumentParser add_argument
        parameters (See https://docs.python.org/2.7/library/argparse.html).  The exception to this 
        rule is that name and switches should be separately defined.  The name of the argument should be
        all caps, using letters numbers and underscores.  This will allow it to serve as a key for the
        GXCONFIG dict and as an environment variable.  
        
        Do not specify 'dest'.  The 'name' will be used for this.
        
        Once collected from the environment, command line or configuration file, values will be returned 
        in the GXCONFIG dict, keyed by the name provided. 
        
        e.g.
        parameterdefs = [
            {  
                'name'          : 'EX_EXAMPLE_NAME',
                'switches'      : ['-x','--example-name'],
                'required'      : 'no',
                'help'          : 'This is an example.',
                'default'       : '',
             },
            {  
                'name'          : 'EX_BOOLEAN',
                'switches'      : ['--boolean'],
                'required'      : 'no',
                'help'          : 'This is an example of a boolean switch.',
                'default'       : False,
                'action'        : 'store_true',
             },
             
        ]
        return parameterdefs
        '''
        pass
    
    
    def finalize(self,gwriter,annotationreader=None):
        '''
        Does the final writing for the writer and closes the file
        '''
        gwriter.write()