from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh.readlines() if line.strip() and not line.startswith("#")]

setup(
    name="eagleview-api-client",
    version="1.0.0",
    author="Satyam Rastogi",
    author_email="satyam.rastogi@example.com",
    description="A Python client library and example programs for interacting with the EagleView API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/satyamrastogi/eagleview-api-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "eagleview-demo=demo_run:main",
        ],
    },
)