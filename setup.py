import os
from setuptools import setup

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3 :: Only
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
Operating System :: Unix
Operating System :: MacOS :: MacOS X
"""

curr_path = os.path.abspath(os.path.dirname(__file__))
setup(
    name='tinyrecord',
    version='0.2.1',
    packages=['tinyrecord'],
    package_data={'tinyrecord': ['py.typed']},
    python_requires='>=3.6',
    install_requires=['tinydb >= 4.0.0'],
    classifiers=filter(None, classifiers.split('\n')),
    zip_safe=True,
    author='Eugene Eeo',
    author_email='141bytes@gmail.com',
    long_description=open(os.path.join(curr_path, 'README.rst'), 'r').read(),
    long_description_content_type='text/x-rst',
    description='Atomic transactions for TinyDB',
    license='MIT',
    keywords='tinydb nosql database transaction',
    url='https://github.com/eugene-eeo/tinyrecord',
)
