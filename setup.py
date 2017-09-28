try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
        name="cerebunit",
        version="0.1.dev",
        author="Lungsi",
        author_email="lungsi.sharma@unic.cnrs-gif.fr",
        packages=["cerebunit",
                  #"cerebunit.file_manager",
                  #"cerebunit.test_manager",
                  "cerebunit.capabilities",
                  "cerebunit.capabilities.cells",
                  "cerebunit.validation_tests",
                  "cerebunit.validation_tests.cells",
                  "cerebunit.validation_tests.cells.PurkinjeCell",
                  #"cerebunit.validation_tests.cells.GranularCell",
                  #"cerebunit.validation_tests.cells.GolgiCell"
                  ],
        #url="",
        license="BSD Clause-3",
        #description="",
        long_description="",
        #install_requires=["sciunit>=0.1.3.1"]
)
