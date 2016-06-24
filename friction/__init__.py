import os

from flask import Flask, render_template, request, send_file, jsonify

from .library import Library

app = Flask(__name__)
library = Library(os.getcwd())


class FrictionError(Exception):
    def __init__(self, status, message):
        super().__init__()
        self.status_code = status
        self.message = message


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
        raise FrictionError(
            400,
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
