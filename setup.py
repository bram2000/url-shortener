from distutils.core import setup

setup(
    name='shortener',
    version='0.1dev0',
    packages=['shortener'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    entry_points={"console_scripts": ["url_shortener=shortener.bootstrap"]},
    install_requires=[
        "flask",
        "sqlalchemy",
        "validators",
        "dozen",
        "requests",
        "contexts",
        "expects",
        "colorama",
        "retrying",
    ],
)
