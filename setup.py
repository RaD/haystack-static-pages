# encoding: utf-8

import os
import sys
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if 'sdist' in sys.argv:
    # clear compiled mo files before building the distribution
    walk = os.walk(os.path.join(os.getcwd(), 'haystack_static_pages/locale'))
    for dirpath, dirnames, filenames in walk:
        if not filenames:
            continue

        if 'django.mo' in filenames:
            os.unlink(os.path.join(dirpath, 'django.mo'))
            print 'unlink', os.path.join(dirpath, 'django.mo')
else:
    # if django is there, compile the po files to mo,
    try:
        import django
    except ImportError:
        pass
    else:
        dir = os.getcwd()
        os.chdir(os.path.join(dir, 'haystack_static_pages'))
        os.system('django-admin.py compilemessages')
        os.chdir(dir)

setup(
    name='haystack-static-pages',
    version='0.3.0',
    description="Static pages for Haystack",
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],
    author='Ruslan Popov',
    author_email='ruslan.popov@gmail.com',
    url='http://github.com/RaD/haystack-static-pages/',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    package_data={
        'haystack_static_pages': ['templates/*']
    },
    # we sure that all are already installed
    #install_requires=[
    #    'django', 'haystack'
    #],
)
