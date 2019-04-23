import setuptools

meta = {}

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("zookeeper_healthcheck/version.py") as f:
    exec(f.read(), meta)

requires = [
]

setuptools.setup(
    name="zookeeper-healthcheck",
    version=meta["__version__"],
    author="Shawn Seymour",
    author_email="shawn@devshawn.com",
    description="A simple healthcheck wrapper to monitor zookeeper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devshawn/zookeeper-healthcheck",
    license="Apache License 2.0",
    packages=["zookeeper_healthcheck"],
    install_requires=requires,
    entry_points={
        "console_scripts": ["zookeeper-healthcheck=zookeeper_healthcheck.main:main"],
    },
    keywords=("zookeeper", "health", "healthcheck", "wrapper", "monitor"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
