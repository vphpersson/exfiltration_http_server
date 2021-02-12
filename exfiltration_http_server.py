#!/usr/bin/env python

from pathlib import PurePath, Path
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from secrets import token_hex
from sys import stderr
from argparse import ArgumentParser
from functools import partial


class HTTPRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, save_directory: Path = Path('.'), use_random_filename: bool = False, **kwargs):
        self.save_directory: Path = save_directory
        self.use_random_filename: bool = use_random_filename
        super().__init__(*args, **kwargs)

    def do_GET(self):
        return

    def do_HEAD(self):
        return

    def do_POST(self):
        url_filename = PurePath(self.path).name

        filename = token_hex(nbytes=16) if (self.use_random_filename or url_filename == '') else url_filename
        save_path = self.save_directory / filename

        if save_path.exists():
            print(f'Could not save file. {save_path} exists.', file=stderr)
            return

        num_bytes = int(self.headers['Content-Length'])

        save_path.write_bytes(self.rfile.read(num_bytes))

        print(f'{save_path.absolute()} - {num_bytes} bytes')


class ExfiltrationHTTPServerArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_argument(
            '-o', '--output-directory',
            help='The output directory where files are to be written.',
            type=Path,
            default=Path('.'),
            metavar='DIRECTORY',
            dest='output_directory'
        )

        self.add_argument(
            '-r', '--use-random-filename',
            help='Use randomly-generated filenames rather than the filename in the URL path.',
            action='store_true'
        )

        self.add_argument(
            '-p', '--port',
            help='The bind port to use.',
            type=int,
            default=8000,
            metavar='PORT',
            dest='bind_port'
        )

        self.add_argument(
            '-b', '--bind',
            help='The bind address to use.',
            default='127.0.0.1',
            metavar='ADDRESS',
            dest='bind_address'
        )


def main():
    args = ExfiltrationHTTPServerArgumentParser().parse_args()

    tcp_server_options = (
        (args.bind_address, args.bind_port),
        partial(
            HTTPRequestHandler,
            save_directory=args.output_directory,
            use_random_filename=args.use_random_filename
        )
    )
    with TCPServer(*tcp_server_options) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
