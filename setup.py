from setuptools import setup, find_packages

setup(
    name='OpticalProperties_scrapping',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scipy',
        'numpy',
        'bs4',
        'requests',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            # Define any console scripts here
        ],
    },
)
