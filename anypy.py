#!/usr/bin/env python3
'''Creates a virtual environment for any version of python'''

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

if not (sys.version_info[0] >= 3 and sys.version_info[1] >= 7):
    raise RuntimeError('You need at least python3.7+ to run this tool!')

ARCHITECTURES = [
    'x86_64_v3',
    'aarch64',
    'armv7',
]

RELEASE_MAP = {
    '3.9.20': '20241016',
    '3.10.15': '20241016',
    '3.11.3': '20230507',
    '3.11.10': '20241016',
    '3.12.7': '20241016',
    '3.13.0': '20241016',
}


def _cached_download(url: str, output: pathlib.Path):
    user_cache = pathlib.Path.home() / '.cache' / 'anypy'
    user_cache.mkdir(parents=True, exist_ok=True)
    file_name = pathlib.Path(url).name
    cached_file = user_cache / file_name
    if not cached_file.exists():
        urllib.request.urlretrieve(url, cached_file)
    shutil.copy2(cached_file, output)


def _get_link(version: str, arch: str) -> str:
    release = RELEASE_MAP[version]
    link = (
        'https://github.com/indygreg/python-build-standalone/releases/download/'
        f'{release}/cpython-{version}+{release}-{arch}-'
        'unknown-linux-gnu-install_only.tar.gz')
    return link


def download(version: str, arch: str, location: pathlib.Path) -> pathlib.Path:
    '''Downloads a standalone `version` of python binary at `location` for the specified
    `arch`
    '''
    location = location / f'.py-{version}'
    print(f'Downloading standalone binary for python {version} at {location}')
    location.mkdir(exist_ok=True, parents=True)
    gitignore = location / '.gitignore'
    gitignore.write_text('*')
    link = _get_link(version, arch)
    with tempfile.TemporaryDirectory() as tmp_:
        pytarf = pathlib.Path(tmp_) / f'py-{version}.tar.zst'
        # urllib.request.urlretrieve(link, pytarf)
        _cached_download(link, pytarf)
        with tarfile.open(pytarf) as pytar:
            pytar.extractall(location)

    major = version.split('.')[0]
    return pathlib.Path(location, 'python', 'bin', f'python{major}')


def _venv(py_bin: pathlib.Path, location: pathlib.Path):
    location = location / '.venv'
    print(f'Creating virtual environment at {location}')
    subprocess.run(f'{py_bin} -m venv --system-site-packages {location}',
                   shell=True,
                   check=True)
    gitignore = location / '.gitignore'
    gitignore.write_text('*')


def venv(version: str, arch: str, location: pathlib.Path):
    '''Download a standalone `version` of python for the `arch` and then create a virtual
    environment using the same python version at `location/.venv`
    '''
    py_bin = download(version, arch, location)
    _venv(py_bin, location)

    venv_activate = location / '.venv' / 'bin' / 'activate'
    print(f'Run python: {py_bin.absolute()}')
    print(f'Activate virtual environment: . {venv_activate.absolute()}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a Python Virtual Environment '
        'with a standalone version of Python',
        epilog='Supported Python versions: '
        f'{list(RELEASE_MAP.keys())}')
    parser.add_argument('version', type=str, help='The Python version')
    parser.add_argument(
        '-l',
        '--location',
        default=pathlib.Path.cwd(),
        type=pathlib.Path,
        help=
        'Where to create the virtual environment (default: current directory)')
    parser.add_argument(
        '-py',
        '--python-only',
        action='store_true',
        help='Only download the Python standalone executable, no venv')
    parser.add_argument('-a',
                        '--arch',
                        choices=ARCHITECTURES,
                        default=ARCHITECTURES[0],
                        help='Specify your system architecture')
    args = parser.parse_args()

    if args.python_only:
        download(args.version, args.arch, args.location)
    else:
        venv(args.version, args.arch, args.location)
