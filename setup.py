import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-jumptoadmin',
    version='0.1.0',
    description="Django templatetag for admins to easily change/delete objects from the public-facing site.",
    long_description=read('README.rst'),
    author='Ryan Berg',
    author_email='ryan.berg@gmail.com',
    license='BSD',
    url='http://github.com/ryanberg/django-jumptoadmin/',
    packages=[
        'jumptoadmin',
        'jumptoadmin.templatetags'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    package_data = {
        'jumptoadmin': [
            'media/jumptoadmin/css/*.css',
            'media/jumptoadmin/img/*.png',
            'media/jumptoadmin/img/*.gif',
            'media/jumptoadmin/js/*.js',
        ]
    },
    zip_safe=False, # required to convince setuptools/easy_install to unzip the package data
)
