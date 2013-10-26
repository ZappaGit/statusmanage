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

import unittest, test_sm_TestSuper, commands, subprocess, time, logging, urllib

logging.basicConfig(filename='smStatusTest_test.log', filemode='w', level=logging.INFO)

"""
TITLE: 
  StatusTest

SUMARY: 
  
"""
class StatusTest(unittest.TestCase):

    def test_wrongInput(self):
	'''
	launch statusmanager.py -t 2
	test wrong input http://localhost:<9959>/bad_input returns ERROR
	'''
	logging.info('  3. StatusTest ')
	logging.info('       test wrong input http://localhost:<9959>/bad_input returns ERROR.')
	global procesSM
	logging.info('  - Launching command "> python statusmanager.py --terminate-after 2"')	
	try:	
	    procesSM = subprocess.Popen(["/usr/bin/python","statusmanager.py", "--terminate-after=2"], stdout=subprocess.PIPE)
	    time.sleep(0.5)
	except IOError as e:
	    logging.info('  - ERROR- Launching command "statusmanager.py --terminate-after"')
            self.assertTrue(False, '  - FAIL- Launching command "statusmanager.py --terminate-after')
	response = urllib.urlopen("http://localhost:9959/bad_input")
	#print response.read().decode('utf-8')	
	time.sleep(0.1)
	self.assertEqual(response.read() ,"ERROR\n")

    def test_30secsOK(self):
	'''
	launch statusmanager.py -t 2
	test  http://localhost:<9959>/status returns the actives list
	'''
	logging.info('  3. StatusTest ')
	logging.info('       test  http://localhost:<9959>/status returns the actives list.')
	global procesSM
	logging.info('  - Launching command "> python statusmanager.py "')	
	try:	
	    procesSM = subprocess.Popen(["/usr/bin/python","statusmanager.py"], stdout=subprocess.PIPE)
	    time.sleep(0.5)
	except IOError as e:
	    logging.info('  - ERROR- Launching command "statusmanager.py --terminate-after"')
            self.assertTrue(False, '  - FAIL- Launching command "statusmanager.py --terminate-after')
	machines = ['a.test','b.test','c.test','d.test','e.test','f.test','g.test','h.test','i.test','j.test','k.test','l.test','o.test','p.test','q.test']
	index = 0
	for item in machines:
	   #print machines[index]
	   response = urllib.urlopen("http://localhost:9959/keepalive?machine="+machines[index])
	   time.sleep(0.1)
	   self.assertEqual(response.read().decode('utf-8'),"OK " + machines[index] + "\n")
	   logging.info(response.read())
	   index = index + 1

