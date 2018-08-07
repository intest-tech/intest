from setuptools import setup, find_packages
import intest

if __name__ == '__main__':
    with open('requirements.txt') as f:
        requirement = f.read().splitlines()

    setup(
        name='intest',
        version=intest.__version__,
        author=intest.__author__,
        author_email=intest.__email__,
        url=intest.__url__,
        description='Testing Library for Python Web Server.',
        install_requires=requirement,
        packages=find_packages(),
    )
