from setuptools import setup, find_packages

setup(
    name="mlops-loan-approval-classification",
    version="0.0.1",
    description="An end-to-end MLFlow for Loan Approval Classification",
    author="Duong",
    author_email="duongng2911@gmail.com", 
    url="https://github.com/duongnguyen-dev/mlops-loan-approval-classification",
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[
        "pyspark==3.5.4",
        "scikit-learn==1.6.0",
        "mlflow==2.19.0",
        "fastapi==0.115.6",
        "seaborn==0.13.2",
        "minio==7.2.13",
        "findspark==2.0.1"
    ],
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