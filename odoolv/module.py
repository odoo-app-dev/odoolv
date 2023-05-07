from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import sys
import json
import os
import pkg_resources

js_file = pkg_resources.resource_filename('odoolv', 'js/log.js')
css_file = pkg_resources.resource_filename('odoolv', 'css/styles.css')
html_file = pkg_resources.resource_filename('odoolv', 'html/index.html')


class WebServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if self.path[1:] != 'favicon.ico':
            # load javascript file
            if self.path[1:] == 'log.js':
                # js_file = os.path.join(current_dir, 'data/js/log.js')
                try:
                    with open(js_file, 'r') as file:
                        file_lines = file.readlines()
                    for line in file_lines:
                        self.wfile.write(line.encode())
                except Exception as e:
                    self.wfile.write(str(e).encode())
            # load style file
            elif self.path[1:] == 'styles.css':
                # css_file = os.path.join(current_dir, 'data/css/styles.css')

                try:
                    with open(css_file, 'r') as file:
                        file_lines = file.readlines()
                    for line in file_lines:
                        self.wfile.write(line.encode())
                except Exception as e:
                    self.wfile.write(str(e).encode())
            # load html file
            else:
                # html_file = os.path.join(current_dir, 'data/html/index.html')
                try:
                    with open(html_file, 'r') as file:
                        file_lines = file.readlines()
                    for line in file_lines:
                        self.wfile.write(line.encode())
                except Exception as e:
                    self.wfile.write(str(e).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
        log_path = post_data.get('log_path')
        log_file = post_data.get('log_file')
        line_no = post_data.get('line_no')

        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.send_header("Access-Control-Allow-Credentials", False)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        if self.path[1:] != 'favicon.ico':
            line_number = int(self.path[1:]) if self.path[1:].isnumeric() else None
            self.wfile.write(self.read_log(log_path, log_file, line_number).encode())

    def read_log(self, log_path, log_file, line_number=None):
        res = {}
        file = os.path.join(log_path, log_file)

        # res['message'] = f'is file:{os.path.isfile(file)}, have access:{os.access(file, os.R_OK)}'

        try:
            if not os.path.isdir(log_path):
                raise Exception('<span style="color:red;">Directory Not Found</span>')
            elif not os.path.isfile(file):
                raise Exception('<span style="color:red;">File Not Found</span>')
            elif not os.access(log_path, os.R_OK):
                raise Exception('<span style="color:red;">No Read Access</span>')
            else:
                with open(file, 'r') as f:
                    logs = tuple(f.readlines())
                file_size = os.path.getsize(file)

        except PermissionError:
            res['message'] = '<span style="color:red;">Permission Error</span>'
        except Exception as e:
            res['file_size'] = 0
            res['length'] = 0
            res['message'] = str(e)
            res = json.dumps(res)
            return res

        length = len(logs)
        if not line_number:
            line_number = length - 10
        data = []
        if line_number and line_number < length:
            for line in logs[line_number:]:
                i = -1
                # print(f'len: {len(line)} BEFORE:\n {line}')

                if line[:40].lower().find('info') >= 0:
                    i = line[:40].lower().find('info')
                    line = line[:i] + '<span style="color:#00a800;">INFO</span>' + line[i + 4:]
                elif line[:40].lower().find('warning') >= 0:
                    i = line[:40].lower().find('warning')
                    line = line[:i] + '<span style="color:#cc8317;">WARNING</span>' + line[i + 7:]
                elif line[:40].lower().find('error') >= 0:
                    i = line[:40].lower().find('error')
                    line = line[:i] + '<span style="color:red;">ERROR</span>' + line[i + 5:]
                # data.append('<p style="margin: 0px;">' + line + '</p>')
                data.append(line)
                # print(f'len: {len(line)} i: {i}   AFTER:\n {line}')

        res['length'] = length
        res['line_number'] = line_number
        res['data'] = data
        res['message'] = '<span style="color:green;">OK</span>'
        res['file_size'] = self.get_formatted_size(file_size)

        res = json.dumps(res)
        # print(f'{"-" * 80}\n{res}\n\n')
        return res


    def get_formatted_size(self, total_size, factor=1024, suffix='B'):
        # looping through the units
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if total_size < factor:
                return f"{total_size:.2f}{unit}{suffix}"
            total_size /= factor
        # returning the formatted video size
        return f"{total_size:.2f}Y{suffix}"
def run():
    try:
        IP_ADDRESS = ''
        PORT = 9000
        server = HTTPServer((IP_ADDRESS, PORT), WebServer)

        print(f'server started on {IP_ADDRESS}:{PORT} ')
        server.serve_forever()
    except KeyboardInterrupt:
        print('server stopped by user')
        server.shutdown()
    except Exception as e:
        print(e)


if __name__ == '__main__':

    run()