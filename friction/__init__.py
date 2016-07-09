import os
from base64 import b32encode

from flask import Flask, render_template, request, send_file, jsonify

from .library import Library, FrictionError

app = Flask(__name__)
library = Library(os.getcwd())


@app.route('/')
def viewer():
    return render_template(
        'viewer.html',
        rotation=request.args.get('r', 'n'),
        filter=request.args.get('f', '').strip(),
        rtl=request.args.get('rtl', ''),
        id=request.args.get('id', ''),

        # needed just to prevent browsers from thinking the page has stayed the
        # same:
        salt=b32encode(os.urandom(2)).decode('utf-8').rstrip('='),
    )


@app.route('/items')
def items():
    identifier = request.args.get('id', None)

    if identifier is not None:
        doujin = library.doujin_for(identifier)
    else:
        doujin = library.choice(request.args.get('f', '').strip())

    if doujin is None:
        raise FrictionError(
            "couldn't find anything in the library matching your filter; try "
            "being less specific"
        )
    return jsonify(doujin.json())


@app.route('/item')
def item():
    doujin = library.doujin_for(request.args['path'])
    return send_file(doujin.pages[int(request.args['page'])])


@app.errorhandler(FrictionError)
def error(e):
    response = jsonify({'message': e.message})
    response.status_code = e.status_code
    return response
