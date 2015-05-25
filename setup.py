from setuptools import setup

setup(name='gpstotz',
      version='0.1',
      install_requires=[
      "rtree",
      "shapely"
      ]
      description='Finds the appropriate timezone for coordinates',
      url='http://github.com/cstich/gpstotz',
      author='Christoph Stich',
      author_email='christoph@stich.xyz',
      license='MIT Licence',
      packages=['geogps'],
      zip_safe=False)
