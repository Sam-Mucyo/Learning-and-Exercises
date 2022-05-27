
'''

Codecademy Python Intermediate Course

'''
import unittest

def get_nearest_exit(row_number):
  if row_number < 15:
    location = 'front'
  elif row_number < 30:
    location = 'middle'
  else:
    location = 'back'
  return location

# Write your code below:
class NearestExitTests(unittest.TestCase):
  def test_row_1(self):
    self.assertEqual(get_nearest_exit(1), 'front', 'The nearest exit to row 1 is in the front!')

  def test_row_20(self):
    self.assertEqual (get_nearest_exit(20), 'middle', 'The nearest exit to row 20 is in the middle!')

  def test_row_40(self):
    self.assertEqual (get_nearest_exit(40), 'back', 'The nearest exit to row 40 is in the back!')


unittest.main()


'''

UNIT TESTING
Assert Methods I: Equality and Membership

Let’s go over three commonly used assert methods for testing equality and 
membership, their general syntax, and their assert statement equivalents.

assertEqual: The assertEqual() method takes two values as arguments and checks 
that they are equal. If they are not, the test fails.

 self.assertEqual(value1, value2)
assertIn: The assertIn() method takes two arguments. It checks that the first 
argument is found in the second argument, which should be a container. If it is
 not found in the container, the test fails.

 self.assertIn(value, container)
assertTrue: The assertTrue() method takes a single argument and checks that
 the argument evaluates to True. If it does not evaluate to True, the test fails.

 self.assertTrue(value)
The equivalent assert statements would be the following:

Method	                              |            Equivalent                  
self.assertEqual(2, 5)	              |        assert 2 == 5
self.assertIn(5, [1, 2, 3])	          |        assert 5 in [1, 2, 3]
self.assertTrue(0)	                  |        assert bool(0) is True
self.assertLess(2, 5)	                |        assert 2 < 5
self.assertAlmostEqual(.22, .225) 	  |        assert round(.22 - .225, 7) == 0

'''



'''
                    INSTRUCTIONS ON USING self.subTest() ====== Code also below
3.
Indent our self.assertIn() call to be inside the for loop and change the first 
argument in self.assertIn() from daily_movie to movie to represent the individual 
movies on each iteration of the loop.

Note: Creating this structure might be okay at first glance (and may even make 
you wonder why we need the context manager), but if we run our test, we will see 
that the test will fail in the middle of our movies collection and won’t check 
the rest (it stops at Black Widow and not Spiral)! This is because like many 
testing frameworks, unittest will fail and stop on the first failure it 
encounters.

Checkpoint 4 Passed
4.
Lastly, under our print statement of movie but before our assertIn() call, 
insert a self.subTest() to wrap our test method. To make sure we can distinguish
 test cases between each movie, pass a single argument of movie into self.subTest().

Don’t forget to preface the context manager with a with statement and indent our 
self.assertIn() statement. Now, we can observe testing multiple movies and if 
they are licensed or not.


                    CODES
'''
import unittest
import entertainment

class EntertainmentSystemTests(unittest.TestCase):

  def test_movie_license(self):
    daily_movies = entertainment.get_daily_movies()
    licensed_movies = entertainment.get_licensed_movies()

    # Write your code below:
    for movie in daily_movies:
      print(movie)
      with self.subTest():
        self.assertIn(movie, licensed_movies)
      

unittest.main()