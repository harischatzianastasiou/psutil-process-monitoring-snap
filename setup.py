from setuptools import find_packages
from setuptools import setup

setup(
        name='flask-temp',
        version='1.0.0',
        description='contains some sample hello world code using Flask',
        author='tchatzian',
        author_email='harischatzi1988@gmail.com',
        url='https://github.com/tchatzian/flask-temp',
        packages=['flask-temp'],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'flask',
            'numpy',
        ],
        )
