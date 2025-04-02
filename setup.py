from setuptools import setup, find_packages

setup(
    name="docmanageapp",
    version="1.0.0",
    description="A Python CLI app for intelligent document classification and summarization.",
    author="Asadbek Rashidov",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "transformers>=4.35.0",
        "torch>=2.0.0",
        "nltk>=3.8.1",
        "pytesseract",
        "python-docx",
        "pillow",
        "PyMuPDF",
        "pandas",
        "openpyxl",
        "fpdf",
        "sumy"
    ],
    entry_points={
        "console_scripts": [
            "docmanage=main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
)
