from setuptools import setup

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
Operating System :: Unix
Operating System :: MacOS :: MacOS X
"""

setup(
    name='tinyrecord',
    version='0.1.4',
    packages=['tinyrecord'],
    classifiers=filter(None, classifiers.split('\n')),
    zip_safe=True,
    author='Eugene Eeo',
    author_email='141bytes@gmail.com',
    description='Atomic transactions for TinyDB',
    license='MIT',
    keywords='tinydb nosql database transaction',
    url='https://github.com/eugene-eeo/tinyrecord',
)
