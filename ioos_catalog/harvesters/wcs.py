#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
ioos_catalog/harvesters/sos.py
Harvester for OGC-SOS Services
'''
from ioos_catalog.harvesters.harvester import Harvester


class WcsHarvest(Harvester):

    def __init__(self, service):
        Harvester.__init__(self, service)

    def harvest(self):
        pass

