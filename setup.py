# utils package for projects in services
# services package for testing
from setuptools import find_packages, setup

install_requires = [
    "apscheduler",
    "python-telegram-bot",
    "pandas>=2, <3",
    "dotenv",
    # "SQLAlchemy>=2.0.23, <3",
    ## gen ai
    "openai>=1, <2",  # might need later, openai client
    "google-generativeai",
    "google-genai",
    "pillow",
    "pydantic-ai==0.0.16",
    "pydantic_core==2.27.2",
    "tiktoken>=0, <1",  # might need later, token counter
    ## file reader
    "python-multipart>=0, <1",  # file upload
    "instructor>=1, <2",  # also output guardrails
    # "nltk>=3, <4",  # might need later, natural language processing
    # "babel>=2, <3", # might need later, international datetime
    "httpx==0.27.2",
    "selenium",
]

extras_require = {
    "dev": [
        # "mlflow",
        # "black>=18.6b4,<21",
        "pytest",
        "pytest-cov",
        "httpx",
        # "pytest-mock>=3.6.1",  # for access to mock fixtures in pytest
    ],
}

if __name__ == "__main__":
    setup(
        name="project-safi",
        version="0.1",
        description="webhook for telegram bot",
        author="Muhammad Nur Ichsan",
        packages=find_packages(),
        install_requires=install_requires,
        extras_require=extras_require,
    )
