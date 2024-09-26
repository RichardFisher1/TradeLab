from setuptools import setup, find_packages

setup(
    name='tradelab',  # Your package name
    version='0.1.0',  # Version of your package
    packages=find_packages(where='src'),  # Look for packages inside 'src'
    package_dir={'': 'src'},  # Root directory for packages is 'src'
    install_requires=[
        'numpy',
        'pandas',
    ],
    include_package_data=True,  # Includes non-code files from MANIFEST.in
    description='A package for backtesting trading strategies',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Specify the format of the README
    url='https://github.com/RichardFisher1/Trading-App',  # Your project URL
    author='Your Name',
    author_email='your.email@example.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
