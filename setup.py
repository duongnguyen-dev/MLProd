from setuptools import setup, find_packages

setup(
    name="mlprod",
    version="0.0.1",
    description="An end-to-end MLFlow for Loan Approval Classification",
    author="Duong",
    author_email="duongng2911@gmail.com", 
    url="https://github.com/duongnguyen-dev/MLProd",
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={},
    include_package_data=True, 
    zip_safe=False,
)