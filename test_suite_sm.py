#!/usr/bin/python
"""
=========================================================
 This is a TestSuite to test the statusmanager.py command
   to run tests: ./test_StatusManager.py  
	or	 python test_StatusManager.py
      (verbose): python test_StatusManager.py -v
=========================================================
 by Diego Izquierdo Fernandez. QualityObjects
"""

import unittest, test_sm_CommandLineInterfaz, sys

def suite():

    suite = unittest.TestSuite()
    suite.addTest (test_sm_CommandLineInterfaz.CommandLineInterfazTest())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(descriptions=True, verbosity=2)
    test_suite = suite()
    runner.run(test_suite)
