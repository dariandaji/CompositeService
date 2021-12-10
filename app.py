import json
import logging
from datetime import datetime
import time
import re

import requests
import grequests
from gevent import monkey
monkey.patch_all()

from flask import Flask, Response
from flask import request, render_template, jsonify
from flask_cors import CORS

import utils.rest_utils as rest_utils
from middleware.service_helper import generate_urls, strip_data, get_order_ids

from pprint import pprint

app = Flask(__name__)
CORS(app)

new_response = {}

@app.route('/orderDetails/<orderID>', methods=["GET"])
def get_order_details(orderID):
    try:
        s = datetime.now()
        # inputs = rest_utils.RESTContext(request)
        data = get_order_ids(orderID)
        urls = generate_urls(data)

        collect_details = []
        collect_responses = []
        for u in urls:
            response = requests.get(u)
            collect_responses.append(response.status_code)
            collect_details.append(json.loads(response.text))

        collect_details = list(map(lambda x: {'data': x} if isinstance(x, list) else x, collect_details))

        for r in collect_responses:
            if r!=200:
                raise Exception("Failed to GET Data!")


        res = strip_data(collect_details)
        res = json.dumps(res, default=str)
        rsp = Response(res, status=200, content_type='application/JSON')
        print(f"Elapsed Time: {datetime.now() - s}")

    except Exception as e:
        print(f"Path: /orderDetails/<orderID>\nException: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')
    return rsp


@app.route('/orderDetailsAsync/<orderID>', methods=["GET"])
def get_order_details_async(orderID):
    try:
        s = datetime.now()
        # inputs = rest_utils.RESTContext(request)
        data = get_order_ids(orderID)
        urls = generate_urls(data)

        collect_details = []
        collect_responses = []

        greqs = (grequests.get(u) for u in urls)
        gres = grequests.map(greqs)

        for g in gres:
            collect_responses.append(g.status_code)
            collect_details.append(json.loads(g.text))

        collect_details = list(map(lambda x: {'data': x} if isinstance(x, list) else x, collect_details))

        for r in collect_responses:
            if r!=200:
                raise Exception("Failed to GET Data!")


        res = strip_data(collect_details)
        res = json.dumps(res, default=str)
        rsp = Response(res, status=200, content_type='application/JSON')
        print(f"Elapsed Time: {datetime.now() - s}")

    except Exception as e:
        print(f"Path: /orderDetailsAsync/<orderID>\nException: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')

    return rsp


@app.route('/orderDetailsComplex/<orderID>', methods=["GET"])
def get_order_details_complex(orderID):
    try:
        location = str(request.base_url) + '/details'
        response = jsonify(f"POST Request will be created at {location}")
        response.status_code = 201
        response.headers['location'] = location

    except Exception as e:
        print(f"Path: /orderDetailsComplex/<orderID>\nException: {e}")
        response = Response("INTERNAL ERROR", status=500, content_type='text/plain')

    return response


@app.route('/orderDetailsComplex/<orderID>/details', methods=["GET"])
def get_order_details_complex_create(orderID):
    try:
        global new_response
        if new_response:
            res = json.loads(new_response.data)
            rsp = Response(json.dumps(res), status=200, content_type='application/JSON')
        else:
            rsp = Response("NOT FOUND", status=404, content_type='text/plain')
    except Exception as e:
        print(f"Path: /orderDetailsComplex/<orderID>/details")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')

    return rsp

# if the complex create function is called, it first returns the location
# where the final data will be stored
# then the following will be called where the data is stored in the new_response
# dictionary. This dictionary can be directly accessed if a GET call is made on the
# location stated in the header of the original response
@app.after_request
def after_request(response):
    global new_response
    new_response = {}
    base_url = ""
    url_root = ""
    if re.match(f"{request.url_root}orderDetailsComplex/[0-9]+$", request.url):
        base_url = request.base_url
        url_root = request.url_root
        location = base_url + '/details'
        response = Response(f"POST Request will be created at {location}",
                            status=201, content_type='text/plain')
    @response.call_on_close
    def process_after_close():
        global new_response
        if base_url and url_root and re.match(f"{url_root}orderDetailsComplex/[0-9]+$", base_url):
            order_id = int(location.split("/")[-2])
            new_response = get_order_details(order_id)
            # response = Response("POST CREATED!", status=201, content_type='text/plain', headers=headers)

    return response

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5003)