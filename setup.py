
from setuptools import setup, find_packages
 
setup(
    name='django-threadedcomments',
    version='0.5.0dev',
    description='A simple yet flexible threaded commenting system',
    author='Eric Florenzano',
    author_email='floguy@gmail.com',
    url='http://code.google.com/p/django-threadedcomments/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
