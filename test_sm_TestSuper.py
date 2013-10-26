
import unittest, subprocess, os, signal, subprocess

class TestSMSuper(unittest.TestCase):

    def setUp(self):
	'''
	delete any previus process status manager
	'''
	p = subprocess.Popen(['ps','-ax'], stdout=subprocess.PIPE)
    	out, err = p.communicate()
    	for line in out.splitlines():
            if 'statusmanager' in line:
                pid = int(line.split(None,3)[0])
		if (pid!=None):
                    os.kill(pid,signal.SIGKILL)

    #def setProcess(process):
#	global procesSM = process

    def tearDown(self):
	procesSM.kill()
	   
