import io, os, re
from setuptools import setup

def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())

setup(
   name="weallcode_robot",
    version="3.0.0",
    url="https://github.com/weallcode/robot",
    license='MIT',

    author="We All Code",
    author_email="hello@weallcode.org",
    
    description="We All Code Robot Client",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",

    packages=["weallcode_robot"],
    install_requires=["bleak"],
    
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)