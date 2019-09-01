from quart import Quart, request, url_for, jsonify, render_template
import os
import json

import logging

app = Quart(__name__)




@app.route('/')
async def index():
    os.system('python sistem_elevator.py')
    with open('elevator.json') as json_file:
        data = json.load(json_file)
        strategs = data

    return await render_template('list.html', strategs=strategs)


@app.route('/clear/')
async def clear():
    try:
        os.remove("elevator.json")
    except:
        return 404

    return index()


if __name__ == '__main__':
    app.run(debug='True')
