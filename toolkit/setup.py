from setuptools import setup, find_packages
import os
import itertools

datadir = "hx3dtoolkit/assets"
datafiles = [[os.path.join(root, f).lstrip("hx3dtoolkit/") for f in files] for root, dirs, files in os.walk(datadir)]
datafiles = [x for x in datafiles if len(x) > 0]
datafiles = list(itertools.chain(*datafiles))
datafiles.extend(["config.yml", "dependencies.yml"])

setup(
    name = "hx3d-toolkit",
    version = "0.1",
    packages = find_packages(),

    scripts = ['hx3d-toolkit'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['colorama', 'pyyaml', 'yamlordereddictloader'],

    package_data = {'hx3dtoolkit': datafiles},

    # metadata for upload to PyPI
    author = "Denis BOURGE",
    author_email = "bourge.denis@gmail.com",
    description = "hx3d management toolkit",
)
