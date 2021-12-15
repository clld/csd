from setuptools import setup, find_packages


setup(
    name='csd',
    version='0.0',
    description='csd',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Robert Forkel, MPI SHH',
    author_email='forkel@shh.mpg.de',
    url='http://csd.clld.org',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'xhtml2pdf',
        'clld>=9',
        'clldmpg>=4.2',
        'sqlalchemy',
        'waitress'
    ],
    extras_require={
        'dev': [
            'flake8',
            'tox'
        ],
        'test': [
            'psycopg2',
            'pytest>=3.1',
            'pytest-clld>=0.4',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="csd",
    entry_points="""\
[paste.app_factory]
main = csd:main
""")
