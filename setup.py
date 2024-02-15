from setuptools import setup, find_packages

# Open and read the contents of the README file
with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name="pyCoopGame",
    version="0.0.3",
    description="various profit allocation methods from cooperative game theory",
    author="Fabian Lechtenberg",
    author_email="fabian.lechtenberg@upc.edu",
    url="https://github.com/flechtenberg/pyCoopGame",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.9, <=3.12",
    install_requires=[
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify the content type of the README
)
