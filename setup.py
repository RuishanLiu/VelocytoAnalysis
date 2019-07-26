try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'VelocytoAnalysis',
    version = '1.1.0',
    description = 'Python library for using RNA velocity in single-cell analysis',
    author = 'Ruishan Liu',
    author_email = 'ruishan@stanford.edu',
    url = 'https://github.com/RuishanLiu/VelocytoAnalysis',
    # download_url = '',
    packages=['VelocytoAnalysis'],
    keywords = ['RNA Velocity', ''],
    install_requires=[
        'numpy',
        'sklearn',
        'time',
        'operator',
        'multiprocessing',
    ],
)
