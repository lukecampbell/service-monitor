from bson.objectid import ObjectId
from datetime import datetime
import time
from ioos_service_monitor import app, db
from ioos_service_monitor.models.base_document import BaseDocument
import requests
from bson.code import Code

@db.register
class Stat(BaseDocument):
    __collection__ = 'stats'
    use_dot_notation = True
    use_schemaless = True

    structure = {
        'service_id'         : ObjectId, # reference to service this statistic is for
        'response_time'      : int,      # response time in ms
        'response_code'      : int,
        'operational_status' : int,      # 1: online 0: offline
        'created'            : datetime,
        'updated'            : datetime,
    }

    default_values = {
        'created': datetime.utcnow
    }

    def ping_service(self):
        s = db.Service.find_one({'_id':self.service_id})
        assert s is not None

        try:
          r = requests.get(s.url)
          self.response_time = r.elapsed.microseconds / 1000
          self.response_code = r.status_code
          self.operational_status = 1 if r.status_code in [200,400] else 0
        except (requests.ConnectionError, requests.HTTPError):
          self.response_code = -1
          self.operational_status = 0

        return str(self)

    @classmethod
    def latest_stats_by_service(self):
        finds = db.Stat.aggregate([{'$group':{'_id':'$service_id',
                                              'when': {'$max':'$created'}}}])

        retval = {}
        for f in finds:
            stat = db.Stat.find_one({'service_id': f['_id'],
                                     'created': f['when']})

            if not stat:
                continue

            retval[f['_id']] = {'response_time':stat.response_time,
                                'response_code':stat.response_code,
                                'operational_status':stat.operational_status,
                                'created':f['when']} 

        return retval

    @classmethod
    def latest_stats_by_service_by_time(self, start_time=None, end_time=None, time_delta=None):
        if end_time is None:
            end_time = datetime.utcnow()

        if start_time is None:
            if time_delta is not None:
                start_time = end_time - time_delta
            else:
                start_time = datetime.utcfromtimestamp(0)   # 1970

        finds = db.Stat.aggregate([{'$match': {'created': {'$gte':start_time, '$lte':end_time}}},
                                   {'$group': {'_id': '$service_id',
                                               'response_time': {'$max':'$response_time'},
                                               'operational_status': {'$max':'$operational_status'}}}])

        retval = {f['_id']:f for f in finds}
        return retval

