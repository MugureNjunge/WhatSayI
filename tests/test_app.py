import unittest
from app.models import Post

class PitchTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the pitch class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_pitch = Post('')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch,Post))

