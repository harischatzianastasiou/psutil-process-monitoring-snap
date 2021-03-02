from setuptools import setup

setup(
        name='psutil-process-monitoring-snap',
        version='1.0.0',
        description='contains some sample hello world code using Flask',
        author='tchatzian',
        author_email='harischatzi1988@gmail.com',
        url='https://github.com/tchatzian/psutil-process-monitoring-snap',
        packages=['psutil-process-monitoring'],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'numpy',
            'pandas',
            'psutil',
            'python-dateutil',
            'pytz',
            'six'
        ],
        )
