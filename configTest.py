import os
import json
import unittest

class TestJson(unittest.TestCase):
    def setUp(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
    
    def testStartupMsg(self):
        self.assertIsInstance(self.config['startupMsg'], bool)

    def testWinWarningMsg(self):
        self.assertIsInstance(self.config['winWarningMsg'], bool)

    def testDefaultTaskbar(self):
        self.assertIsInstance(self.config['defaultTaskbar'], bool)

    def testAutoConnect(self):
        self.assertIsInstance(self.config['autoConnect'], bool)

    def testKeepAlive(self):
        self.assertIsInstance(self.config['keepAlive'], bool)

if __name__ == '__main__':
    unittest.main()


