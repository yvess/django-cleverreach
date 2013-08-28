#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup
import os
import setuplib

packages, package_data = setuplib.find_packages('email_registration')

setup(name='django-cleverreach',
    version=__import__('cleverreach').__version__,
    description='A Django API for cleverreach.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author=u'Simon Bächler',
    author_email='sb@feinheit.ch',
    url='http://github.com/feinheit/django-cleverreach/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=packages,
    package_data=package_data,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
