from setuptools import setup

setup(
    name='tlogs',
    version="0.0.1",
    iurl="https://github.com/xyzsss/tlogs",
    packages=['tlogs'],
    license='GPL',
    author='xyzsss',
    author_email='exuxu50@@gmail.com',
    description='Application for log your minds or events for lookup later',
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
