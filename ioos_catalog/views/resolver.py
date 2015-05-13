#!/usr/bin/env python
'''
ioos_catalog/views/resolver.py
'''

from ioos_catalog import app, db
from bson import json_util
from flask import jsonify
import json

@app.route('/api/resolver/asset/<string:asset_id>', methods=['GET'])
def get_resolver_asset(asset_id):
    '''
    Returns a JSON response for all matching datasets to the URN
    '''
    datasets = db.Dataset.find({u"uid":asset_id, u"services":{u"$elemMatch":{u"service_type":u"SOS"}}})
    datasets = [json.dumps(d, default=json_util.default) for d in datasets]

    response_string = '{"datasets":[%s]}' % ','.join(datasets)
    return response_string, 200, {'Content-Type':'application/json'}


