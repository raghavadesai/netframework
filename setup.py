from setuptools import setup, find_packages

setup(
    name="netframework",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'pyOpenSSL>=23.0.0',
        'cryptography>=41.0.0',
    ],
    python_requires=">=3.7",
)