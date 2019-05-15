from contextlib import contextmanager
from io import DEFAULT_BUFFER_SIZE
from typing import BinaryIO
from urllib.request import urlopen


def download_file_from_ftp(file_url: str, file_path: str):
    """Download file from an FTP URL to a file. The file is loaded chunk by
    chunk."""
    with open_ftp_file(file_url) as ftp_fp:
        with open(file_path, 'wb') as fs_fp:
            while True:
                chunk = ftp_fp.read(DEFAULT_BUFFER_SIZE)
                if not chunk:
                    break
                fs_fp.write(chunk)


def download_ftp_text(file_url: str) -> str:
    """Download FTP file to memory return it as string (ASCII encoding is
    assumed).

    :param file_url: file URL which must start with ftp://
    """
    with open_ftp_file(file_url) as fp:
        return fp.read().decode('ASCII')


@contextmanager
def open_ftp_file(file_url: str) -> BinaryIO:
    """Open an FTP URL for reading.

    :param file_url: file URL which must start with ftp://
    """
    if not file_url.startswith('ftp://'):
        raise ValueError('Only FTP URLs are accepted.')

    try:
        fp = urlopen(file_url, timeout=30)
        yield fp
    finally:
        fp.close()
