from setuptools import setup, find_packages

setup(name='mozping_explorer',
      version='0.0.1',
      author='Frank Bertsch',
      author_email='fbertsch@mozilla.com',
      description='Exploration functions for mozilla telemetry pings',
      url='https://github.com/fbertsch/mozping_explorer',
      packages=find_packages(),
      tests_require=['pytest'])
