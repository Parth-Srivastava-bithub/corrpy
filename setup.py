from setuptools import setup, find_packages

setup(
    name='corrpy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'IPython'
    ],
    author='YellowForest',
    description='Correlation analysis tool with smart interpretation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Parthdsaiml/corrpy',  # optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
