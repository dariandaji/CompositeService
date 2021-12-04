import json
import logging
from datetime import datetime

import requests
from flask import Flask, Response
from flask import request, render_template, jsonify
from flask_cors import CORS

import utils.rest_utils as rest_utils
from middleware.service_helper import generate_urls, strip_data

from pprint import pprint

app = Flask(__name__)
CORS(app)

# sample_call = {
#     "userID": 1,
#     "productID": 15,
#     "orderID": 1
# }

@app.route('/orderDetails', methods=["GET"])
def get_order_details():
    try:
        s = datetime.now()
        inputs = rest_utils.RESTContext(request)
        data = inputs.data
        urls = generate_urls(data)

        collect_details = []
        collect_responses = []
        for u in urls:
            response = requests.get(u)
            collect_responses.append(response.status_code)
            collect_details.append(json.loads(response.text))

        for r in collect_responses:
            if r!=200:
                raise Exception("Failed to GET Data!")


        res = strip_data(collect_details)
        res = json.dumps(res, default=str)
        rsp = Response(res, status=200, content_type='application/JSON')
        print("Running Time: ")
        return rsp

    except Exception as e:
        print(f"Path: /orderDetails\nException: {e}")
        rsp = Response("INTERNAL ERROR", status=500, content_type='text/plain')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)