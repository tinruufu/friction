import json
import os

from flask import Flask, render_template, request, send_file

from .library import Library

app = Flask(__name__)
library = Library(os.getcwd())


@app.route('/')
def viewer():
    return render_template(
        'viewer.html',
        rotation=request.args.get('r'),
        filter=request.args.get('f', ''),
    )


@app.route('/items')
def items():
    doujin = library.choice(request.args['f'])
    if doujin is None:
        raise NotImplementedError(
            'your filter was too specific and im too lazy to handle that '
            'gracefully'
        )
    return json.dumps(doujin.json())


@app.route('/item')
def item():
    doujin = library.doujin_for(request.args['path'])
    return send_file(doujin.pages[int(request.args['page'])])
