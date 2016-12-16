#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
ioos_catalog/harvesters/wms.py
Harvester for OGC-WMS Services
'''
from ioos_catalog.harvesters.harvester import Harvester


class WmsHarvest(Harvester):

    def __init__(self, service):
        Harvester.__init__(self, service)

    def harvest(self):
        pass

