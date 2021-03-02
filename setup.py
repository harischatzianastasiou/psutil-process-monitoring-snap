import os

from setuptools import setup

this = os.path.dirname(os.path.realpath(__file__))


def read(name):
    with open(os.path.join(this, name)) as f:
        return f.read()

setup(
        name='psutil-process-monitoring-snap',
        version='1.0.0',
        description='Process monitoring using cross-platform library psutil',
        author='tchatzian',
        author_email='harischatzi@tutanota.com',
        url='https://github.com/tchatzian/psutil-process-monitoring-snap',
        packages=['psutil-process-monitoring-snap'],
        install_requires=read('requirements.txt'),
        include_package_data=True,
        zip_safe=False,
)
