from setuptools import setup, find_packages
from typing import List


EPHINE_DOT= '-e .'

def get_requirements() -> List[str]:
    requirements = []
    try:

        with open('requirements.txt') as f:
            lines = f.read().strip()

        for line in lines.split('\n'):
            if line != EPHINE_DOT:
                requirements.append(line)
        return requirements

    except FileNotFoundError:
        raise FileNotFoundError('requirements.txt')



setup(
    name='PolicyAI',
    version='1.0.0',
    author='Vikrant',
    author_email='patilvikrant275@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)