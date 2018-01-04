"""This is the setup file for the project. The standard setup rules apply:
   python setup.py build
   sudo python setup.py install
"""
#from distutils.core import setup
from setuptools import find_packages
from setuptools import setup

am_description = (
    u'autoMatching is a simple tool for demonstrate MERGE procedure of two'
    u'matchings. Using it, you can easily generate or demonstrate examples'
    u'for the MERGE of two matchings.')

setup(
    name=u'autoMatching',
    version=u'2017.03',
    url='',
    license='',
    author='Long Gong',
    author_email='long.github@gmail.com',
    description='Automatically demonstrate merge of two matchings',
    long_description=am_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=[u'serena_demo_ctl'],
    data_files=[
        (u'.', [u'matching_template.tex', u'cycle_template_flexible.tex'])
    ],
    install_requires=frozenset([
        u'Flask',
        u'Flask-script',
        u'numpy',
        u'networkx',
        u'Send2Trash',
        u'Jinja2',
    ])
)
