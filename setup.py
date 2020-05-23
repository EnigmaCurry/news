import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setuptools.setup(
    name="news", # Replace with your own username
    version="0.0.1",
    author="EnigmaCurry",
    author_email="ryan@enigmacurry.com",
    description="A 'news' aggregator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enigmacurry/news",
    packages=setuptools.find_packages(),
    classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "newscatcher @ git+https://github.com/EnigmaCurry/newscatcher.git#egg=newscatcher",
        "Mako",
        "click",
        "css-html-js-minify",
        "pyyaml",
        "beautifulsoup4",
        "boto3"
    ],
    package_data={'news': ['blunt.css', 'templates/*']},
    include_package_data=True,
    entry_points={
        'console_scripts':[
            'news = news.news:main'
        ]
    }
)
