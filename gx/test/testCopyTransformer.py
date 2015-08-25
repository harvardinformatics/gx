'''
Created on Aug 24, 2015

@author: aaronkitzmiller
'''
import os,sys
import unittest

from hex.cmd import Command

class Test(unittest.TestCase):


    def setUp(self):
        self.inputfilename = 'ce10sample.fa'
        self.inputdata = '''>chrIV
GAATATGAAATAGGAGTTCGAATCTTGAAATGCGAGAAAGAGGGGGCGCCAGCAACATGC
CTTAACTTGTCGGGGACCTCTTTAAAAAAAAAGAAATTTATCTGAAATGATATGGATTCA
AAAACTTCAAAATGAGTTTCTCCTAGTGCCAAGCAAACTACTTGGCAAATACATACATTA
TTCAAAAAGTACATAACATA
>chrX
ttttgaaaaaagttcgtgtgtattagcatcaggctcgggtaggcgcgatgtcggcaaacg
ttgctttaaaaacaggcaggcaggcgtcttggcgcctatatgaaagccttaGGGAAGACA
TAACTTATGCCGTTTCTTTTCGACTAATAGCTGATTTTTTTTCAATTCTACCCTTGCTCG
AATCGCACATATTTGAATGC
>chrII
AGATGGTCTGTGTAGCCGGCGGCGAACCAACACAAAAATGAGTCGCCTTATATACCCCCC
GCGCGCACGAGTGGTCGGGGGTCGATCGGAAAACCGGTTGAGACCGGCGGCGGGAGATCC
ATCTACGTCTCCGCGTCTCTCTCACTGTCCGACTGTTGTCGTCGGCCACCCGTATGTATG
TGGTGGACCCTCTAAGGTTC
>chrM
TTTTTAAATATGTTTTGAAAACATGTTTTGAGGTAACTCGTAGTTTTTAAGAGTTAGTTT
AATATAGAATTGTTGACTGTTAATCAAAAGGTGTACCTCTTAATATAAGAGTTTAGTTTA
AGTTAAAACGTTAGATTGTAAATCTAAAGATTATTGCTCTTGATAATTTTAGTTTTACTT
ATAGTTATTTTAATGATGAT
>chrI
TAATCGCTTGTTATGCATAAATCCAATTTCAAAAATAATTTCTTCAAATTTTCGTTCACC
TAATAATACCTTTATCCGTCCGTAGACAAATCCACACGCACCTGTTCATGGGTAATCCAA
CCAAAATCCCACGCTTTTTAAGTAACCGATGCGCTCCATAGGAGCATAATTGGTGTGTGC
AACGATATGGGATGTGCTCT
>chrV
TTTCCGGAAGCCTAGAAAAATTCCAGATATTTTTTTCATTGCTCTGGCTAATTGTAATGA
AGCTTTTACAACTGTGTACTGCACTATAGTGATTTTCCAAAAAATTAACAAATTAAAAAA
AAACGTTTGATCTGTTTCGTGCTAATTACTTCCTTTTTTATTCATAAGTTGTGTTATGAC
GAAGATTACATATTTTTTGA
>chrIII
AAGAGTGAGAAGTTCGTGCCACCGACCATCAAAACTTTTTCCAATTTTATTTCATCACCA
ACGTTCAATGGGAGATTTCCCTCCATATTGATTAAATCGCCATCACTGACCTGAAAGATT
TTGGGGTTTTCGAAAAATCGATTTAAAAAAAAACTAATTTTCATATTTTGCAAATGTTCT
TCAGAAAAATTTGGATTTTA
'''
        


    def tearDown(self):
#         try: 
#             #os.remove(self.inputfilename)
#         except Exception:
#             pass
        pass

    def testCopyTransformer(self):
        '''
        Test copy of a genome to another file, first an identical copy, then with altered output column count
        '''
        f = open(self.inputfilename,'w')
        f.write(self.inputdata)
        f.close()
        
        # test exact copy
        params = {
            'GX_INPUT_GENOME_FILE'   : self.inputfilename,
            'GX_FASTA_COLUMN_NUMBER' : 60,
            'GX_OUTPUT_GENOME_FILE'  : 'out.fa',
            'GX_SEGMENT_SIZE'        : 100,
            'GX_TRANSFORMER'         : 'CopyTransformer',
        }
        
        cmd = Command('gxf.py --debug --genome-transformer {GX_TRANSFORMER} -i {GX_INPUT_GENOME_FILE} -o {GX_OUTPUT_GENOME_FILE} -s {GX_SEGMENT_SIZE} --output-columns {GX_FASTA_COLUMN_NUMBER}'.format(**params))
        [returncode,stdout,stderr] = cmd.run()
        self.assertTrue(returncode == 0,"gxf.py failed: %s" % stderr)
        
        f = open(params["GX_OUTPUT_GENOME_FILE"],'r')
        outputstr = f.read()
        f.close()
        self.assertTrue(outputstr == self.inputdata, "Input and output don't match.")

        # test slightly different column number
        outputdata = '''>chrIV
GAATATGAAATAGGAGTTCGAATCTTGAAATGCGAGAAAGAGGGGGCGCCAGCAACATGCC
TTAACTTGTCGGGGACCTCTTTAAAAAAAAAGAAATTTATCTGAAATGATATGGATTCAAA
AACTTCAAAATGAGTTTCTCCTAGTGCCAAGCAAACTACTTGGCAAATACATACATTATTC
AAAAAGTACATAACATA
>chrX
ttttgaaaaaagttcgtgtgtattagcatcaggctcgggtaggcgcgatgtcggcaaacgt
tgctttaaaaacaggcaggcaggcgtcttggcgcctatatgaaagccttaGGGAAGACATA
ACTTATGCCGTTTCTTTTCGACTAATAGCTGATTTTTTTTCAATTCTACCCTTGCTCGAAT
CGCACATATTTGAATGC
>chrII
AGATGGTCTGTGTAGCCGGCGGCGAACCAACACAAAAATGAGTCGCCTTATATACCCCCCG
CGCGCACGAGTGGTCGGGGGTCGATCGGAAAACCGGTTGAGACCGGCGGCGGGAGATCCAT
CTACGTCTCCGCGTCTCTCTCACTGTCCGACTGTTGTCGTCGGCCACCCGTATGTATGTGG
TGGACCCTCTAAGGTTC
>chrM
TTTTTAAATATGTTTTGAAAACATGTTTTGAGGTAACTCGTAGTTTTTAAGAGTTAGTTTA
ATATAGAATTGTTGACTGTTAATCAAAAGGTGTACCTCTTAATATAAGAGTTTAGTTTAAG
TTAAAACGTTAGATTGTAAATCTAAAGATTATTGCTCTTGATAATTTTAGTTTTACTTATA
GTTATTTTAATGATGAT
>chrI
TAATCGCTTGTTATGCATAAATCCAATTTCAAAAATAATTTCTTCAAATTTTCGTTCACCT
AATAATACCTTTATCCGTCCGTAGACAAATCCACACGCACCTGTTCATGGGTAATCCAACC
AAAATCCCACGCTTTTTAAGTAACCGATGCGCTCCATAGGAGCATAATTGGTGTGTGCAAC
GATATGGGATGTGCTCT
>chrV
TTTCCGGAAGCCTAGAAAAATTCCAGATATTTTTTTCATTGCTCTGGCTAATTGTAATGAA
GCTTTTACAACTGTGTACTGCACTATAGTGATTTTCCAAAAAATTAACAAATTAAAAAAAA
ACGTTTGATCTGTTTCGTGCTAATTACTTCCTTTTTTATTCATAAGTTGTGTTATGACGAA
GATTACATATTTTTTGA
>chrIII
AAGAGTGAGAAGTTCGTGCCACCGACCATCAAAACTTTTTCCAATTTTATTTCATCACCAA
CGTTCAATGGGAGATTTCCCTCCATATTGATTAAATCGCCATCACTGACCTGAAAGATTTT
GGGGTTTTCGAAAAATCGATTTAAAAAAAAACTAATTTTCATATTTTGCAAATGTTCTTCA
GAAAAATTTGGATTTTA
'''
        params['GX_FASTA_COLUMN_NUMBER'] = 61
        cmd = Command('gxf.py --debug --genome-transformer {GX_TRANSFORMER} -i {GX_INPUT_GENOME_FILE} -o {GX_OUTPUT_GENOME_FILE} -s {GX_SEGMENT_SIZE} --output-columns {GX_FASTA_COLUMN_NUMBER}'.format(**params))
        [returncode,stdout,stderr] = cmd.run()
        self.assertTrue(returncode == 0,"gxf.py failed: %s" % stderr)
        
        f = open(params["GX_OUTPUT_GENOME_FILE"],'r')
        outputstr = f.read()
        f.close()
        self.assertTrue(outputstr == outputdata, "Input and output for 61 columns don't match.")
        
        # Remove the output file
        os.remove(params['GX_OUTPUT_GENOME_FILE'])
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()