from distutils.core import setup

setup(
    name='django-backup',
    version='0.2',
    license='BSD',
    description='A Way to Run Remote Backups Through the Django Admin',
    author='Adam Miskiewicz',
    author_email='adam@level2designs.com',
    url='http://github.com/level2designs.com/django-backup/tree',
    packages=[
        'backup',
    ],
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)

