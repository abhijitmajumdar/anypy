#!/usr/bin/env python3
'''Creates a virtual environment for any version of python'''

from __future__ import annotations

import argparse
import pathlib
import platform
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
    '3.8.9': '20210415',
    '3.8.10': '20210506',
    '3.8.11': '20210724',
    '3.8.12': '20220227',
    '3.8.13': '20220802',
    '3.8.14': '20221002',
    '3.8.15': '20221106',
    '3.8.16': '20230726',
    '3.8.17': '20230826',
    '3.8.18': '20240224',
    '3.8.19': '20240814',
    '3.8.20': '20240909',
    '3.9.4': '20210415',
    '3.9.5': '20210506',
    '3.9.6': '20210724',
    '3.9.7': '20211017',
    '3.9.10': '20220227',
    '3.9.11': '20220318',
    '3.9.12': '20220502',
    '3.9.13': '20220802',
    '3.9.14': '20221002',
    '3.9.15': '20221106',
    '3.9.16': '20230507',
    '3.9.17': '20230726',
    '3.9.18': '20240224',
    '3.9.19': '20240814',
    '3.9.20': '20241016',
    '3.10.0': '20211017',
    '3.10.2': '20220227',
    '3.10.3': '20220318',
    '3.10.4': '20220528',
    '3.10.5': '20220630',
    '3.10.6': '20220802',
    '3.10.7': '20221002',
    '3.10.8': '20221106',
    '3.10.9': '20230116',
    '3.10.11': '20230507',
    '3.10.12': '20230726',
    '3.10.13': '20240224',
    '3.10.14': '20240814',
    '3.10.15': '20241016',
    '3.11.1': '20230116',
    '3.11.3': '20230507',
    '3.11.4': '20230726',
    '3.11.5': '20230826',
    '3.11.6': '20231002',
    '3.11.7': '20240107',
    '3.11.8': '20240224',
    '3.11.9': '20240814',
    '3.11.10': '20241016',
    '3.12.0': '20231002',
    '3.12.1': '20240107',
    '3.12.2': '20240224',
    '3.12.3': '20240415',
    '3.12.4': '20240726',
    '3.12.5': '20240814',
    '3.12.6': '20240909',
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
    if arch not in ARCHITECTURES:
        raise RuntimeError(f'Unsupported architecture: {arch}')
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
    parser.add_argument(
        '-a',
        '--arch',
        choices=ARCHITECTURES,
        default=platform.machine(),
        help=
        'Specify your system architecture. Uses platform.machine() if unspecified'
    )
    args = parser.parse_args()

    if args.python_only:
        download(args.version, args.arch, args.location)
    else:
        venv(args.version, args.arch, args.location)
