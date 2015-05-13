#!/usr/bin/env python
'''
ioos_catalog/views/resolver.py
'''

from ioos_catalog import app, db
from bson import json_util
from flask import jsonify, render_template, url_for
from glob import glob
from ioos_catalog.views.ra import provider_info as p_info
from collections import OrderedDict
import json

def dot_get(o, path):
    i = path.split('.', 1)
    if len(i) > 1:
        return dot_get(o[i[0]], i[1])
    return o[i[0]]

def load_assets(key, path):
    assets_json = 'Assets.json'
    with open(assets_json, 'r') as f:
        assets = json.loads(f.read())

    assets = dot_get(assets, key)
    files = []
    for filepath in assets[path]:
        if '*' not in filepath:
            files.append(filepath)
        else:
            for glob_path in glob(filepath):
                files.append(glob_path)
    # Strip off the beginning piece
    files = [f.replace('ioos_catalog', '') for f in files]
    return files

def load_javascripts(key, template_name):
    path = 'ioos_catalog/static/js/compiled/%s.js' % template_name
    if app.config['DEBUG']:
        scripts_list = []
        for js_file in load_assets(key, path):
            script = '<script src="%s" type="text/javascript"></script>' % js_file
            scripts_list.append(script)
        scripts = '\n'.join(scripts_list)
        return scripts
    path = path.replace('ioos_catalog', '')
    return '<script src="%s" type="text/javascript"></script>' % path

def load_css(key, template_name):
    path = 'ioos_catalog/static/css/compiled/%s.css' % template_name
    if app.config['DEBUG']:
        scripts_list = []
        for css_file in load_assets(key, path):
            script = '<link href="%s" rel="stylesheet" type="text/css" />' % css_file
            scripts_list.append(script)
        scripts = '\n'.join(scripts_list)
        return scripts
    path = path.replace('ioos_catalog', '')
    return '<link href="%s" rel="stylesheet" type="text/css" />' % path

@app.route('/api/resolver/config.json', methods=['GET'])
def get_resolver_config():
    navbar_img = url_for('.static', filename='img/ioos.png')
    inventory_link = url_for('inventory')
    services_link = url_for('services')
    datasets_link = url_for('datasets')
    gliders_link = url_for('gliders')
    metadatas_link = url_for('metadatas')
    catalog_map_link = url_for('catalog_map')
    help_link = url_for('help')

    return jsonify(locals())

@app.route('/api/providers', methods=['GET'])
@app.route('/api/providers/', methods=['GET'])
def get_providers():
    '''
    Returns a JSON response that lists the providers
    '''
    ra_list, national_list = [], []
    for key in p_info:
        if p_info[key].get('provider_type') == 'national':
            national_list.append(key)
        #assume unset provider types are regional by default
        elif p_info[key].get('provider_type', 'regional') == 'regional':
            ra_list.append(key)

    response = {}
    response['ra_providers'] = OrderedDict([(provider, url_for('show_ra', provider=provider)) for provider in sorted(ra_list)])
    response['national_partners'] = OrderedDict([(provider, url_for('show_ra', provider=provider)) for provider in sorted(national_list)])
    return jsonify(response)


@app.route('/api/resolver/asset/<string:asset_id>', methods=['GET'])
def get_resolver_asset(asset_id):
    '''
    Returns a JSON response for all matching datasets to the URN
    '''
    datasets = db.Dataset.find({u"uid":asset_id, u"services":{u"$elemMatch":{u"service_type":u"SOS"}}})
    datasets = [json.dumps(d, default=json_util.default) for d in datasets]

    response_string = '{"datasets":[%s]}' % ','.join(datasets)
    return response_string, 200, {'Content-Type':'application/json'}

@app.route('/resolver/asset/<string:asset_id>')
def show_resolver(asset_id):
    '''
    Renders the asset resolver template
    '''
    scripts = load_javascripts('main.js', 'resolver')
    css = load_css('main.css', 'resolver')
    return render_template('resolver.html', scripts=scripts, css=css, asset_id=asset_id)


