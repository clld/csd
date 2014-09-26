import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'clld',
    'clldmpg',
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'zope.sqlalchemy',
    'gunicorn',
    'psycopg2',
    'waitress',
    ]

tests_require = [
    'WebTest >= 1.3.1', # py3 compat
    'mock',
]

setup(name='csd',
      version='0.0',
      description='csd',
      long_description='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      test_suite="csd",
      entry_points="""\
[paste.app_factory]
main = csd:main
""",
      )
