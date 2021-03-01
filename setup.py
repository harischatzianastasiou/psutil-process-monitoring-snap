from setuptools import find_packages
from setuptools import setup

setup(
        name='psutil-process-monitoring-snap',
        version='1.0.0',
        description='Process monitoring using cross-platform library psutil',
        author='tchatzian',
        author_email='harischatzi@tutanota.com',
        url='https://github.com/tchatzian/psutil-process-monitoring-snap',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'psutil',
            'pandas',
        ]
