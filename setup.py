from setuptools import setup, find_packages

setup(
    name = "Corrpy",
    version = "0.2.8",
    packages = find_packages(),
    install_requires = [
        'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'IPython', 'together', 'scikit-learn'
    ],
    author = 'YellowForest',
    description='Correlation analysis tool with smart interpretation',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Parthdsaiml/corrpy',  # optional
    license='BSD 3-Clause',  # Use BSD license here if that's the correct one
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',  # Corrected license classifier
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)
