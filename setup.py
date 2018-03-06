from setuptools import setup, find_packages

setup(name='joye',
      version='0.1',
      description='Flexible and declarative tool for creating and evaluating machine learning models based on Scikit-learn.',
      url='https://github.com/olchikd/joye',
      author='Olga Druchek',
      author_email='olchikd@gmail.com',
      license='GNU',
      packages=find_packages(),
      include_package_data=True,
      scripts=['play.py', 'predict.py'],
      zip_safe=False)
