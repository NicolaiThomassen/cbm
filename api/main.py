#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of CbM (https://github.com/ec-jrc/cbm).
# Author    : Guido Lemoine, Konstantinos Anastasakis
# Credits   : GTCAP Team
# Copyright : 2021 European Commission, Joint Research Centre
# License   : 3-Clause BSD


import os
import json
import logging
from decimal import Decimal
from functools import wraps
from flasgger import Swagger
from werkzeug.utils import secure_filename
from logging.handlers import TimedRotatingFileHandler
from flask import (Flask, request, send_from_directory, make_response,
                   render_template, flash, redirect, jsonify, abort)


from scripts import query_handler as qh
from scripts import users

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SWAGGER'] = {
    'title': 'CbM API',
    'uiversion': 3
}

# Enable upload page.
UPLOAD_ENABLE = False  # True or False


# -------- Core functions ---------------------------------------------------- #

# Authentication decorator.
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and users.auth(auth.username, auth.password) is True:
            return f(*args, **kwargs)
        return make_response(
            'Could not verify.', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated


swag = Swagger(app, decorators=[auth_required],
               template_file='templates/flasgger.json')


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)


@app.route('/query/', methods=['GET'])
@auth_required
def query():
    return "DIAS API"


@app.route('/query/options', methods=['GET'])
@auth_required
def options():
    """
    Get the available options (for current the user).
    ---
    tags:
      - options
    responses:
      200:
        description: Returns a dictionary of available options
        schema:
            type: object
    """
    try:
        with open('config/options.json', 'r') as f:
            api_options = json.load(f)
        return make_response(jsonify(api_options), 200)
    except Exception as err:
        return str(err)


# -------- Queries - Chip Images --------------------------------------------- #

@app.route('/dump/<unique_id>/<png_id>')
# @auth_required
def dump(unique_id, png_id):
    try:
        return send_from_directory(f"files/dump/{unique_id}", png_id)
    except FileNotFoundError:
        abort(404)


@app.route('/query/chipsByLocation', methods=['GET'])
@auth_required
def chipsByLocation_query():
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # Start by getting the request IP address
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        rip = request.environ['REMOTE_ADDR']
    else:
        rip = request.environ['HTTP_X_FORWARDED_FOR']

    lon = request.args.get('lon')
    lat = request.args.get('lat')

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if 'lut' in request.args.keys():
        lut = request.args.get('lut')
    else:
        lut = '5_95'

    if 'bands' in request.args.keys():
        bands = request.args.get('bands')
    else:
        bands = 'B08_B04_B03'

    if 'plevel' in request.args.keys():
        plevel = request.args.get('plevel')
    else:
        plevel = 'LEVEL2A'

    unique_id = f"dump/{rip}E{lon}N{lat}L{lut}_{plevel}_{bands}".replace(
        '.', '_')

    data = qh.getChipsByLocation(
        lon, lat, start_date, end_date, unique_id, lut, bands, plevel)

    if data:
        return send_from_directory(f"files/{unique_id}", 'dump.html')
    else:
        return json.dumps({})


@app.route('/query/backgroundByLocation', methods=['GET'])
@auth_required
def backgroundByLocation_query():
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # Start by getting the request IP address
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        rip = request.environ['REMOTE_ADDR']
    else:
        rip = request.environ['HTTP_X_FORWARDED_FOR']

    lon = request.args.get('lon')
    lat = request.args.get('lat')

    if 'chipsize' in request.args.keys():
        chipsize = request.args.get('chipsize')
    else:
        chipsize = '256'

    if 'extend' in request.args.keys():
        chipextend = request.args.get('extend')
    else:
        chipextend = '256'

    if 'tms' in request.args.keys():
        tms = request.args.get('tms')
    else:
        tms = 'Google'

    if 'iformat' in request.args.keys():
        iformat = request.args.get('iformat')
    else:
        iformat = 'tif'

    unique_id = f"dump/{rip}E{lon}N{lat}_{chipsize}_{chipextend}_{tms}".replace(
        '.', '_')

    data = qh.getBackgroundByLocation(
        lon, lat, chipsize, chipextend, tms, unique_id, iformat)

    if data:
        if 'raw' in request.args.keys():
            return 1
        else:
            return send_from_directory(f"files/{unique_id}", 'dump.html')
    else:
        return json.dumps({})


@app.route('/query/chipsByParcelId', methods=['GET'])
@auth_required
def chipsByParcelId_query():
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # Start by getting the request IP address
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        rip = request.environ['REMOTE_ADDR']
    else:
        rip = request.environ['HTTP_X_FORWARDED_FOR']

    aoi = request.args.get('aoi')
    year = request.args.get('year')
    parcelid = request.args.get('pid')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if 'lut' in request.args.keys():
        lut = request.args.get('lut')
    else:
        lut = '5_95'

    if 'bands' in request.args.keys():
        bands = request.args.get('bands')
    else:
        bands = 'B08_B04_B03'

    if 'plevel' in request.args.keys():
        plevel = request.args.get('plevel')
    else:
        plevel = 'LEVEL2A'

    unique_id = f"dump/{rip}_{aoi}{year}_{parcelid}_{lut}_{plevel}_{bands}".replace(
        '.', '_')

    data = qh.getChipsByParcelId(aoi, year, parcelid, start_date, end_date,
                                 unique_id, lut, bands, plevel)

    if data:
        return send_from_directory(f"files/{unique_id}", 'dump.html')
    else:
        return json.dumps({})


@app.route('/query/rawChipByLocation', methods=['GET'])
@auth_required
def rawChipByLocation_query():
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # Start by getting the request IP address
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        rip = request.environ['REMOTE_ADDR']
    else:
        rip = request.environ['HTTP_X_FORWARDED_FOR']

    lon = request.args.get('lon')
    lat = request.args.get('lat')

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    band = request.args.get('band')

    if 'plevel' in request.args.keys():
        plevel = request.args.get('plevel')
    else:
        plevel = 'LEVEL2A'

    if 'chipsize' in request.args.keys():
        chipsize = request.args.get('chipsize')
    else:
        chipsize = '1280'

    unique_id = f"dump/{rip}E{lon}N{lat}_{plevel}_{chipsize}_{band}".replace(
        '.', '_')

    data = qh.getRawChipByLocation(
        lon, lat, start_date, end_date, unique_id, band, chipsize, plevel)

    if data:
        return send_from_directory(f"files/{unique_id}", 'dump.json')
    else:
        return json.dumps({})


# -------- Queries - Time Series --------------------------------------------- #

@app.route('/query/parcelTimeSeries', methods=['GET'])
@auth_required
def parcelTimeSeries_query():
    aoi = request.args.get('aoi')
    year = request.args.get('year')
    parcelid = request.args.get('pid')
    tstype = request.args.get('tstype')
    band = None

    if 'band' in request.args.keys():
        band = request.args.get('band')
    data = qh.getParcelTimeSeries(aoi, year, parcelid, tstype, band)
    if not data:
        return json.dumps({})
    elif len(data) == 1:
        return json.dumps(dict(zip(list(data[0]),
                                   [[] for i in range(len(data[0]))])))
    else:
        return json.dumps(dict(zip(list(data[0]),
                                   [list(i) for i in zip(*data[1:])])),
                          cls=CustomJsonEncoder)


@app.route('/query/parcelPeers', methods=['GET'])
@auth_required
def parcelPeers_query():
    parcelTable = request.args.get('parcels')
    pid = request.args.get('pid')
    distance = 1000.0
    maxPeers = 10
    if 'distance' in request.args.keys():
        distance = float(request.args.get('distance'))
    if 'max' in request.args.keys():
        maxPeers = int(request.args.get('max'))

    if distance > 5000.0:
        distance = 5000.0
    if maxPeers > 100:
        maxPeers = 100

    data = qh.getParcelPeers(parcelTable, pid, distance, maxPeers)
    if not data:
        return json.dumps({})
    elif len(data) == 1:
        return json.dumps(dict(zip(list(data[0]),
                                   [[] for i in range(len(data[0]))])))
    else:
        return json.dumps(dict(zip(list(data[0]),
                                   [list(i) for i in zip(*data[1:])])))


@app.route('/query/parcelByLocation', methods=['GET'])
@auth_required
def parcelByLocation_query():
    parcelTable = request.args.get('parcels')
    lon = request.args.get('lon')
    lat = request.args.get('lat')
    withGeometry = False

    if 'withGeometry' in request.args.keys():
        withGeometry = True if request.args.get(
            'withGeometry') == 'True' else False
    data = qh.getParcelByLocation(parcelTable, lon, lat, withGeometry)
    if not data:
        return json.dumps({})
    elif len(data) == 1:
        return json.dumps(dict(zip(list(data[0]),
                                   [[] for i in range(len(data[0]))])))
    else:
        return json.dumps(dict(zip(list(data[0]),
                                   [list(i) for i in zip(*data[1:])])))


@app.route('/query/parcelById', methods=['GET'])
@auth_required
def parcelById_query():
    parcelTable = request.args.get('parcels')
    withGeometry = False

    if 'withGeometry' in request.args.keys():
        withGeometry = True if request.args.get(
            'withGeometry') == 'True' else False

    parcelid = request.args.get('parcelid')
    data = qh.getParcelById(parcelTable, parcelid, withGeometry)

    if not data:
        return json.dumps({})
    elif len(data) == 1:
        return json.dumps(dict(zip(list(data[0]),
                                   [[] for i in range(len(data[0]))])))
    else:
        return json.dumps(dict(zip(list(data[0]),
                                   [list(i) for i in zip(*data[1:])])))


@app.route('/query/parcelsByPolygon', methods=['GET'])
@auth_required
def parcelsByPolygon_query():
    parcelTable = request.args.get('parcels')
    withGeometry = False
    only_ids = True

    if 'withGeometry' in request.args.keys():
        withGeometry = True if request.args.get(
            'withGeometry') == 'True' else False

    if 'only_ids' in request.args.keys():
        only_ids = True if request.args.get(
            'only_ids') == 'True' else False

    polygon = request.args.get('polygon')
    data = qh.getParcelsByPolygon(parcelTable, polygon, withGeometry, only_ids)

    if not data:
        return json.dumps({})
    elif len(data) == 1:
        return json.dumps(dict(zip(list(data[0]),
                                   [[] for i in range(len(data[0]))])))
    else:
        return json.dumps(dict(zip(list(data[0]),
                                   [list(i) for i in zip(*data[1:])])))


# -------- Uploader ---------------------------------------------------------- #

app.config['UPLOAD_FOLDER'] = 'uploads'


def allowed_file(filename):
    # Allow specific file types.
    return '.' in filename and \
           filename.split('.', 1)[1].lower() in ['zip', 'tar.gz']


@app.route('/upload', methods=['GET', 'POST'])
@auth_required
def upload_file():
    # Show upload page only if the uploader is enabled.
    if UPLOAD_ENABLE is True:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if not allowed_file(file.filename):
                flash('Not allowed file type selection')
                return render_template('not_allowed.html')
            if file.filename == '':
                flash('No selected file')
                return render_template('no_selection.html')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('The file is uploaded.')
                return render_template('uploaded.html')
        return render_template('upload.html')
    else:
        return ''


# To download an uploaded file (http://0.0.0.0/uploads/FILENAME.zip).
@app.route('/uploads/<filename>')
@auth_required
def uploaded_file(filename):
    if UPLOAD_ENABLE is True:
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename)


# ======== Main ============================================================== #
if __name__ == "__main__":
    logname = 'logs/app.log'
    handler = TimedRotatingFileHandler(logname, when='midnight', interval=1)
    handler.suffix = '%Y%m%d'
    logger = logging.getLogger('tdm')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    app.run(debug=True, use_reloader=True,
            host='0.0.0.0', port=5000, threaded=True)