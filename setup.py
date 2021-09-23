from pkg_resources import parse_requirements
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    REQUIREMENTS = [str(req) for req in parse_requirements(f.read())]

setup(
    name="calendar-app",
    version="1.0.0",
    entry_points={'console_scripts': ["calendar = calendar_app.app:main"]},
    install_requires=REQUIREMENTS,
    description="App to provide insights about your calendar data",
    packages=find_packages(exclude=["test", "test.*"])
)
