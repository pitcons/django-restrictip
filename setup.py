import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-restrictip",
    version = "1.0.1",
    url = 'http://github.com/pitcons/django-restrictip',
    license = 'GPL v3',
    description = "An ip blocker by regexp and ip range for Django apps.",
    long_description = read('README'),

    author = 'Petr Timofeev',
    author_email = 'petr.cons@gmail.com',

    packages = find_packages('src'),
    package_dir = {'': 'src'},
    
    install_requires = ['setuptools'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
