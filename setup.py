try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'VelocytoAnalysis',
    version = '1.1.0',
    packages=['VelocytoAnalysis'],
    license='MIT',
    description = 'Python library for using RNA velocity in single-cell analysis',
    url = 'https://github.com/RuishanLiu/VelocytoAnalysis',
    author = 'Ruishan Liu',
    author_email = 'ruishan@stanford.edu',
    install_requires=[
        'numpy',
        'sklearn'
    ],
)
