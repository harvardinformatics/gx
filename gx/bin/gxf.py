#!/usr/bin/env python
# encoding: utf-8
'''
gxf -- Executable that runs the Genome Transformer

Genome Transformer is a framework that supports the use of transformers to convert one genome into another.  


@author:     Aaron Kitzmiller

@copyright:  2015 Harvard University. All rights reserved.

@license:    license

@contact:    aaron_kitzmiller@harvard.edu
'''

import sys,os,traceback

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from gx import getClassFromName

__all__ = []
__version__ = 0.1
__date__ = '2015-06-25'


#
# dict containing the final set of configuration variables
# 
GXCONFIG = {}
GXDEBUG = False
    
def getTransformerClasses():
    """
    Returns a dictionary of transformer class objects keyed by name.  
    pkgutil.iter_modules is used to interrogate the transformers directory.  
    Any class with a 'processSegment' class will be returned
    """
    
    # Add options from the batch systems
    # First, iterate through the batchSystems path to get all of the available modules
    # Then, for any class that has the getOptionData class method, use it to get 
    # data to create options.
    import pkgutil
    import inspect
    import gx.transformer as transformer
    
    transformerClasses = {}
    # Load the modules in the transformer path.  Use iter_modules to avoid 
    # sub packages
    for loader, name, is_pkg in pkgutil.iter_modules(transformer.__path__):
        module = loader.find_module(name).load_module(name)
    
        for name, value in inspect.getmembers(module):
            
            # Look for the getOptionData method
            for methodname, methoddata in inspect.getmembers(value, predicate=inspect.ismethod):
                if methodname == 'processSegment':
                    transformerClasses[name] = value
    return transformerClasses
   
def main(argv=None): 
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_version_message = '%%(prog)s %s' % (program_version)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Aaron Kitzmiller on %s.
  Copyright 2015 Harvard University. All rights reserved.

  Licensed under the Gnu General Public License v. 2
  http://www.gnu.org/licenses/gpl-2.0.html

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        
        #
        # Initialize the configuration with defaults and user config file
        #
        parameterdefs = [
            {
                'name'      : 'GX_DEBUG',
                'switches'  : ['--debug'],
                'help'      : 'Debug mode.  You get tracebacks and whatnot.',
                'action'    : 'store_true',
             },
            {
                'name'      : 'GX_GENOME_READER',
                'switches'  : ['--genome-reader'],
                'required'  : False,
                'help'      : 'The genome reader class.',
                'default'   : 'PyfastaReader',
             },
            {
                'name'      : 'GX_GENOME_WRITER',
                'switches'  : ['--genome-writer'],
                'required'  : False,
                'help'      : 'The genome writer class.',
                'default'   : 'BufferedFastaWriter',
                
             },
            {
                'name'      : 'GX_SEGMENT_DISPATCHER',
                'switches'  : ['--segment-dispatcher'],
                'required'  : False,
                'help'      : 'The segment dispatcher class.',
                'default'   : 'SerialDispatcher',
             },
            {
                'name'      : 'GX_ANNOTATION_READER',
                'switches'  : ['--annotation-reader'],
                'required'  : False,
                'help'      : 'The annotation reader class.',
                'default'   : 'BigBedAnnotationReader'
             },
            {
                'name'      : 'GX_INPUT_GENOME_FILE',
                'switches'  : ['-i','--input-file'],
                'help'      : 'Input genome fasta file.',
             },
            {
                'name'      : 'GX_SEGMENT_SIZE',
                'switches'  : ['-s','--segment-size'],
                'help'      : 'Size in bases of genome segments.'
             },
            {
                'name'      : 'GX_TRANSFORMER',
                'switches'  : ['-x','--genome-transformer'],
                'help'      : 'The genome transformer',
             },
            {
                'name'      : 'GX_OUTPUT_GENOME_FILE',
                'switches'  : ['-o','--output-file'],
                'help'      : 'The output fasta file',
             }
        ]
        
        # Get the transformer classes and 
        # query for parameter defs
        transformers = getTransformerClasses()
        for name, transformer in transformers.iteritems():
            pdefs = transformer.getParameterDefs()
            if pdefs:
                parameterdefs = parameterdefs + pdefs
            
        # Check for environment variable values
        # Set to 'default' if they are found
        for parameterdef in parameterdefs:
            if os.environ.get(parameterdef['name'],None) != None:
                parameterdef['default'] = os.environ.get(parameterdef['name'])
                
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        
        # Use the parameterdefs for the ArgumentParser
        for parameterdef in parameterdefs:
            switches = parameterdef.pop('switches')
            if not isinstance(switches, list):
                switches = [switches]
                
            #Gotta take it off for add_argument
            name = parameterdef.pop('name')
            parameterdef['dest'] = name
            if 'default' in parameterdef:
                parameterdef['help'] += '  [default: %s]' % parameterdef['default']
            parser.add_argument(*switches,**parameterdef)
            
            # Gotta put it back on for later
            parameterdef['name'] = name
            
            
        args = parser.parse_args()
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")
        
        # Retrieve the parameter values into the GXCONFIG hash
        for parameterdef in parameterdefs:
            GXCONFIG[parameterdef['name']] = getattr(args,parameterdef['name'])
            
        # Set debug mode
        if 'GX_DEBUG' in GXCONFIG and GXCONFIG['GX_DEBUG']:
            GXDEBUG = True
            
        # Create the specified GenomeReader / GenomeWriter and AnnotationReader
        greader = None
        gwriter = None
        annotreader = None
        segdispatcher = None
        transformer = None
        
        # Create the genome reader
        if 'GX_GENOME_READER' not in GXCONFIG:
            raise Exception('GX_GENOME_READER must be defined')

        # Add the default package to the class if it is not a full package name
        if GXCONFIG['GX_GENOME_READER'].find('.') == -1:
            GXCONFIG['GX_GENOME_READER'] = 'gx.io.%s' % GXCONFIG['GX_GENOME_READER']
        greaderclass = getClassFromName(GXCONFIG['GX_GENOME_READER'])
        greader = greaderclass(GXCONFIG)
        
        
        # Create the genome writer
        if 'GX_GENOME_WRITER' not in GXCONFIG:
            raise Exception('GX_GENOME_WRITER must be defined')
        
        if GXCONFIG['GX_GENOME_WRITER'].find('.') == -1:
            GXCONFIG['GX_GENOME_WRITER'] = 'gx.io.%s' % GXCONFIG['GX_GENOME_WRITER']
        gwriterclass = getClassFromName(GXCONFIG['GX_GENOME_WRITER'])
        gwriter = gwriterclass(GXCONFIG)
        

        # Create the segment dispatcher
        if 'GX_SEGMENT_DISPATCHER' not in GXCONFIG:
            raise Exception('GX_SEGMENT_DISPATCHER must be defined')
        
        if GXCONFIG['GX_SEGMENT_DISPATCHER'].find('.') == -1:
            GXCONFIG['GX_SEGMENT_DISPATCHER'] = 'gx.dispatcher.%s' % GXCONFIG['GX_SEGMENT_DISPATCHER']
        segdispatcherclass = getClassFromName(GXCONFIG['GX_SEGMENT_DISPATCHER'])
        segdispatcher = segdispatcherclass(GXCONFIG)

        
        # Annotation readers are optional
        # The GX_ANNOTATION_READERs key has a list of reader type:source pairs
#         if 'GX_ANNOTATION_READER' in GXCONFIG:
#             try:
#                 annotreader = AnnotationReader(**GXCONFIG)
#             except Exception, e:
#                 raise Exception('Unable to create annotation reader %s: %s' 
#                     % (GXCONFIG['GX_ANNOTATION_READER'], str(e)))
#         
        
        # Create the transformer
        if 'GX_TRANSFORMER' not in GXCONFIG:
            raise Exception('A genome transformer (GX_TRANSFORMER) must be defined')
        
        if GXCONFIG['GX_TRANSFORMER'].find('.') == -1:
            GXCONFIG['GX_TRANSFORMER'] = 'gx.transformer.%s' % GXCONFIG['GX_TRANSFORMER']
        txclass = getClassFromName(GXCONFIG['GX_TRANSFORMER'])
        transformer = txclass(GXCONFIG)
        
        
        '''
        # Iterate over the segments of the Genome and pass them on to each
        transformer
        '''
        for seg in greader.segments():
            segdispatcher.dispatch(seg,transformer,annotreader,gwriter)
            
        segdispatcher.finalize(transformer,annotreader,gwriter)
                
                
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        if 'GX_DEBUG' in GXCONFIG and GXCONFIG['GX_DEBUG']:
            sys.stderr.write(traceback.format_exc() + "\n")
            sys.stderr.write(repr(GXCONFIG) + "\n")
        sys.stderr.write("  for help use --help\n")
        return 2

if __name__ == "__main__":
    sys.exit(main())