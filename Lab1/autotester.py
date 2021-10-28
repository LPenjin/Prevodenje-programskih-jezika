import os
import unittest
from unittest.mock import patch
from unittest import TestCase
import os
import GLA
import analizator.LA

class Test(TestCase):
    # get_input will return 'yes' during this test
    primjeri = os.listdir('test_primjeri/')

    @patch('GLA.get_input', return_value='yes')
    @patch('LA.get_input', return_value='no')
    def test_answer_no(self, input):
        self.assertEqual(answer(), 'you entered no')

if __name__ == '__main__':
    unittest.main()