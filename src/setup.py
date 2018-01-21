from setuptools import setup, find_packages

setup(name='pythonegardia',
      version='1.0.34',
      description='Python 3 support for Egardia / Woonveilig alarm',
      url='https://github.com/jeroenterheerdt/python-egardia',
      author='Jeroen ter Heerdt',
      license='MIT',
      install_requires=['requests>=2.0'],
      tests_require=['mock'],
      test_suite='tests',
      packages=find_packages(exclude=["dist", "*.test", "*.test.*", "test.*", "test"]),
      zip_safe=True)
