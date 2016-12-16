#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
ioos_catalog/harvesters/harvester.py
Base harvester class
'''
from ioos_catalog import app, db
from datetime import datetime
from functools import wraps


def context_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with app.app_context():
            return f(*args, **kwargs)
    return wrapper


def res2dict(r):
    cl = []
    if getattr(r, 'children', None):
        cl = map(res2dict, r.children)

    return {
        'name': unicode(r.name),
        'score': float(r.value[0]),
        'maxscore': float(r.value[1]),
        'weight': int(r.weight),
        'children': cl
    }


def unicode_or_none(thing):
    try:
        if thing is None:
            return thing
        else:
            try:
                return unicode(thing)
            except:
                return None
    except:
        return None


def get_common_name(data_type):
    """Map names from various standards to return a human readable form"""
    # TODO: should probably split this into DAP and SOS specific mappings
    mapping_dict = {
        # Remap UNKNOWN, None to Unspecified
        None: 'Unspecified',
        'UNKNOWN': 'Unspecified',
        '(NONE)': 'Unspecified',
        # Rectangular grids remap to the CF feature type "grid"
        'grid': 'Regular Grid',
        'Grid': 'Regular Grid',
        'GRID': 'Regular Grid',
        'RGRID': 'Regular Grid',
        # Curvilinear grids
        'CGRID': 'Curvilinear Grid',
        # remap some CDM `cdm_data_type`s to equivalent CF-1.6 `featureType`s
        'trajectory': 'Trajectory',
        'point': 'Point',
        # UGrid to unstructured grid
        'ugrid': 'Unstructured Grid',
        # Buoys
        'BUOY': 'Buoy',
        # time series
        'timeSeries': 'Time Series'
    }

    # Get the common name if defined, otherwise return initial value
    return unicode(mapping_dict.get(data_type, data_type))


class Harvester(object):

    def __init__(self, service):
        self.service = service

    @context_decorator
    def save_ccheck_and_metadata(self, service_id, checker_name, ref_id, ref_type, scores, metamap):
        """
        Saves the result of a compliance checker scores and metamap document.

        Will be called by service/station derived methods.
        """
        if not (scores or metamap):
            return

        metadata = db.Metadata.find_one({'ref_id': ref_id})
        if metadata is None:
            metadata = db.Metadata()
            metadata.ref_id = ref_id
            metadata.ref_type = unicode(ref_type)

        if isinstance(scores, tuple):  # New API of compliance-checker
            scores = scores[0]
        cc_results = map(res2dict, scores)

        # @TODO: srsly need to decouple from cchecker
        score = sum(((float(r.value[0]) / r.value[1]) * r.weight for r in scores))
        max_score = sum((r.weight for r in scores))

        score_doc = {'score': float(score),
                     'max_score': float(max_score),
                     'pct': float(score) / max_score}

        update_doc = {'cc_score': score_doc,
                      'cc_results': cc_results,
                      'metamap': metamap}

        for mr in metadata.metadata:
            if mr['service_id'] == service_id and mr['checker'] == checker_name:
                mr.update(update_doc)
                break
        else:
            metarecord = {'service_id': service_id,
                          'checker': unicode(checker_name)}
            metarecord.update(update_doc)
            metadata.metadata.append(metarecord)

        metadata.updated = datetime.utcnow()
        metadata.save()

        return metadata
