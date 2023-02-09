import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nullstream",
    version="0.1",
    author="Boris Goncharov",
    author_email="goncharov.boris@physics.msu.ru",
    description="Null stream tools for gravitational-wave astronomy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bvgoncharov/nullstream",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
