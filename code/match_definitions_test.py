# API unit testing

import unittest
import match_definitions

class MatchDefinitionTestCase(unittest.TestCase):
    def test_something(self):
        match = match_definitions.Match("../dataset/test/2014-2-2-Arsenal-Crystal_Palace.json")
        self.assertEqual(match.getHomeSide().getName(), 'Arsenal')

if __name__ == '__main__':
    unittest.main()
