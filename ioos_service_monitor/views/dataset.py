import json
import urlparse
from datetime import datetime, timedelta
from pymongo import DESCENDING
from flask.ext.wtf import Form
from flask import render_template, redirect, url_for, request, flash, jsonify, Response
from wtforms import TextField, IntegerField, SelectField

from ioos_service_monitor import app, db, scheduler
from ioos_service_monitor.models.stat import Stat
from ioos_service_monitor.tasks.stat import ping_service_task
from ioos_service_monitor.tasks.reindex_services import reindex_services


class DatasetFilterForm(Form):
    asset_type = SelectField('Asset Type', choices=[(u'BUOY', u'BUOY')])

@app.route('/datasets/', defaults={'filter_type':None}, methods=['GET'])
@app.route('/datasets/filter/<filter_type>', methods=['GET'])
def datasets(filter_type):
    filters = {}

    if filter_type is not None and filter_type != "null":
        filters['asset_type'] = filter_type

    f          = DatasetFilterForm()
    datasets   = list(db.Dataset.find(filters))
    assettypes = db.Dataset.aggregate({'$group' : {'_id' : '$asset_type' }})

    return render_template('datasets.html', datasets=datasets, form=f, assettypes=assettypes, filters=filters)

@app.route('/datasets/<ObjectId:dataset_id>', methods=['GET'])
def show_dataset(dataset_id):
    dataset = db.Dataset.find_one({'_id':dataset_id})
    return render_template('show_dataset.html', dataset=dataset)

@app.route('/datasets/removeall', methods=['GET'])
def removeall():
    dataset = db.Dataset.find()
    for d in dataset:
        d.delete()
    return redirect(url_for('datasets'))