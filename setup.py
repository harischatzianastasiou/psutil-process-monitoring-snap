from setuptools import setup

setup(
        name='psutil-process-monitoring-snap',
        version='1.0.0',
        description='Process monitoring using cross-platform library psutil',
        author='tchatzian',
        author_email='harischatzi@tutanota.com',
        url='https://github.com/tchatzian/psutil-process-monitoring-snap',
        packages=['psutil-process-monitoring-snap'],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'psutil',
            'pandas',
        ],
        scripts=['psutil-process-monitoring-snap/psutil-process-monitoring-snap.py'],
        )

