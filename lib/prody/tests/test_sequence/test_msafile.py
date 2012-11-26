#!/usr/bin/python
# -*- coding: utf-8 -*-
# ProDy: A Python Package for Protein Dynamics Analysis
# 
# Copyright (C) 2010-2012 Ahmet Bakan
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = 'Ahmet Bakan, Anindita Dutta'
__copyright__ = 'Copyright (C) 2010-2012 Ahmet Bakan'

from unittest import TestCase

from StringIO import StringIO
import os

from numpy import array, log, zeros, char
from numpy.testing import assert_array_equal, dec

from prody.tests.test_datafiles import *
from prody.tests import TEMPDIR
from prody import MSA, MSAFile, parseMSA, LOGGER, writeMSA

LOGGER.verbosity = None

FASTA = parseMSA(pathDatafile('msa_Cys_knot.fasta'))
SELEX = parseMSA(pathDatafile('msa_Cys_knot.slx'))
STOCK = parseMSA(pathDatafile('msa_Cys_knot.sth'))
FASTA_LIST = list(MSAFile(pathDatafile('msa_Cys_knot.fasta')))
SELEX_LIST = list(MSAFile(pathDatafile('msa_Cys_knot.sth')))
STOCK_LIST = list(MSAFile(pathDatafile('msa_Cys_knot.sth')))

class TestMSAFile(TestCase):
    
    def testMSAFile(self):
        
        self.assertListEqual(FASTA_LIST, SELEX_LIST)
        self.assertListEqual(FASTA_LIST, STOCK_LIST)

    def testWriteFasta(self):
        
        fasta = StringIO()
        with MSAFile(fasta, 'w', format='fasta') as out:
            for label, seq in MSAFile(pathDatafile('msa_Cys_knot.fasta'), 
                                      split=False):
                out.write(label, seq)
        fasta.seek(0)
        fasta_list = list(MSAFile(fasta))
        self.assertListEqual(FASTA_LIST, fasta_list)        
   
    def testWriteSelex(self):
        
        selex = StringIO()
        with MSAFile(selex, 'w', format='selex') as out:
            for label, seq in MSAFile(pathDatafile('msa_Cys_knot.slx'), 
                                      split=False):
                out.write(label, seq)
        selex.seek(0)
        selex_list = list(MSAFile(selex))
        self.assertListEqual(SELEX_LIST, selex_list) 
        
    def testWriteStockholm(self):
        
        stock = StringIO()
        with MSAFile(stock, 'w', format='stock') as out:
            for label, seq in MSAFile(pathDatafile('msa_Cys_knot.sth'), 
                                      split=False):
                out.write(label, seq)
        stock.seek(0)
        stock_list = list(MSAFile(stock))
        self.assertListEqual(STOCK_LIST, stock_list)      

class TestParseMSA(TestCase):
    
    def testArray(self):
        
        assert_array_equal(FASTA._getArray(), SELEX._getArray())
        assert_array_equal(SELEX._getArray(), STOCK._getArray())

    def testIterator(self):
        
        self.assertListEqual(list(FASTA), list(SELEX))
        self.assertListEqual(list(FASTA), list(STOCK))

    def testMapping(self):
        
        self.assertDictEqual(FASTA._mapping, SELEX._mapping)
        self.assertDictEqual(FASTA._mapping, STOCK._mapping)
        
class TestWriteMSA(TestCase):
    
    def testFASTA(self):
        filename = writeMSA((TEMPDIR + '/test.slx'), FASTA)
        SELEX_WRITE = parseMSA(pathDatafile(filename))
        self.assertListEqual(list(SELEX), list(SELEX_WRITE))
        if os.path.isfile(filename):
            os.remove(filename)
            
    def testSELEX(self):
        filename = writeMSA((TEMPDIR + '/test.fasta.gz'), SELEX)
        FASTA_WRITE = list(MSAFile(pathDatafile(filename)))
        self.assertListEqual(list(FASTA), list(FASTA_WRITE))
        if os.path.isfile(filename):
            os.remove(filename)