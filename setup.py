from setuptools import find_packages
from setuptools import setup

setup(
        name='psutil-process-monitor-snap',
        version='1.0.0',
        description='Process monitoring using cross-platform library psutil',
        author='tchatzian',
        author_email='harischatzi@tutanota.com',
        url='https://github.com/tchatzian/psutil-process-monitoring-snap',
        packages=['psutil_snap'],
        include_package_data=True,
        zip_safe=False,
        scripts=['psutil_snap/psutil_monitor'],
)
