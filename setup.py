from setuptools import setup, find_packages
import unittest


def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('joey', pattern='*_tests.py')
    return test_suite


setup(name='joey',
      version='0.1',
      description='Flexible and declarative tool for creating and evaluating machine learning models based on Scikit-learn.',
      url='https://github.com/olchikd/joey',
      author='Olga Druchek',
      author_email='olchikd@gmail.com',
      license='GNU',
      packages=find_packages(),
      include_package_data=True,
      scripts=['play.py', 'evaluate.py', 'predict.py'],
      zip_safe=False,
      test_suite='setup.test_suite',
      tests_require=['nose', 'coverage', 'mock'])
