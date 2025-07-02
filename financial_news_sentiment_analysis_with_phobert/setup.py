# setup.py

import setuptools # type: ignore

setuptools.setup(
    name="PhoBert_sentiment",
    version="0.1.0",
    description="Pipeline fine-tune PhoBERT sentiment classifier",
    author="Victor Nguyen",
    author_email="quanghuy71847@gmail.com",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "transformers",
        "torch",
        "datasets",
        "pandas",
        "scikit-learn",
        "beautifulsoup4",
        "vnstock",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "run-all=main:cli",
        ],
    },
)
