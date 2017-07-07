from setuptools import setup, find_packages

setup(name='python-egardia',
      version='1.0.3',
      description='Python 3 support for Egardia / Woonveilig alarm',
      url='https://github.com/jeroenterheerdt/python-egardia',
      author='Jeroen ter Heerdt',
      license='MIT',
      install_requires=['requests>=2.0'],
      tests_require=['mock'],
      test_suite='tests',
      packages=find_packages(exclude=["dist", "*.test", "*.test.*", "test.*", "test"]),
      zip_safe=True)
