from setuptools import setup, find_packages

setup(
    name='bigquery-sdk',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'google-cloud-bigquery',
        'google-auth',
    ],
    description='SDK for interacting with BigQuery across multiple GCP projects',
    author='Jaimin Parmar',
    author_email='jaiminparmar7827@gmail.com'
)
