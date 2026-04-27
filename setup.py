import sys
import os
import codecs
import setuptools

packages = ['rflib', 'vstruct', 'vstruct.defs']
mods = []
pkgdata = {}
scripts = ['rfcat',
           'rfcat_server',
           'rfcat_msfrelay',
'CC-Bootloader/rfcat_bootloader',
           ]

# store the GIT revision in an rflib python file
try:
    REV = os.popen('./revision.sh').readline().encode('UTF-8')
    if len(REV):
        open('rflib/rflib_version.py', 'wb').write(b"RFLIB_VERSION=%s" % REV)

    RFCAT_VERSION = open('VERSION').read().strip()
except:
    sys.excepthook(*sys.exc_info())

requirements = open('requirements.txt').read().split('\n')


# Readme function to show readme as a description in pypi
def readme():
    with codecs.open('README.md', encoding='utf-8') as f:
        return f.read()


setuptools.setup  (name  = 'rfcat',
        version          = RFCAT_VERSION,
        description      = "the swiss army knife of subGHz",
        long_description = readme(),
        author           = 'atlas of d00m',
        author_email     = 'atlas@r4780y.com',
        url              = 'https://github.com/atlas0fd00m/rfcat',
        download_url     = 'https://github.com/atlas0fd00m/rfcat/archive/v1.9.1.tar.gz',
        keywords         = ['radio', 'subghz', 'cc1111', 'chipcon', 'hacking', 'reverse engineering'],
        packages         = setuptools.find_packages(),
        package_data     = pkgdata,
        ext_modules      = mods,
        scripts          = scripts,
        install_requires = requirements,
        extras_require={
            'specan': [
                'PySide6>=6.4',
            ]
        },
        classifiers      = [
                            'Development Status :: 5 - Production/Stable',
                            'Intended Audience :: Telecommunications Industry',
                            'Topic :: Communications',
                            'License :: OSI Approved :: BSD License',
                            'Programming Language :: Python :: 3',
                            'Programming Language :: Python :: 3.8',
                            'Programming Language :: Python :: 3.9',
                            'Programming Language :: Python :: 3.10',
                            'Programming Language :: Python :: 3.11',
                            'Programming Language :: Python :: 3.12',
                           ],
        python_requires  = '>=3.8'
        )
