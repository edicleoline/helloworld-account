from setuptools import setup, find_namespace_packages

setup(
    name='helloworld-account',
    version='0.1',
    packages=find_namespace_packages(include=['helloworld.*']),
    namespace_packages=['helloworld'],
)