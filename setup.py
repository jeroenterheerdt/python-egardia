from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pythonegardia',
      version='1.0.50',
      description='Python 3 support for Egardia / Woonveilig alarm',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/jeroenterheerdt/python-egardia',
      author='Jeroen ter Heerdt',
      license='MIT',
      install_requires=['requests>=2.0'],
      tests_require=['mock'],
      test_suite='tests',
      packages=find_packages(exclude=["dist", "*.test", "*.test.*", "test.*", "test"]),
      include_package_data=True,
      zip_safe=True)
