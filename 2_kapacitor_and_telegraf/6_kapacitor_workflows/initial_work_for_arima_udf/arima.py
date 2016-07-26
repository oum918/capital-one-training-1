import sys
import time
import json
from kapacitor.udf.agent import Agent, Handler
from kapacitor.udf import udf_pb2

import pandas as pd
import numpy as np
import datetime as dt
from statsmodels.tsa.arima_model import ARIMA

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger()



def arima(ts, forecast_window):
    logger.info(ts)
    start = int(ts.count() - 1)
    end = int(start + forecast_window)

    ts_log = np.log(ts)
    model = ARIMA(ts_log, order=(0, 1, 2))
    results = model.fit(disp=-1)
    prediction = results.predict(start=start, end=end, dynamic=True)
    future = pd.Series(prediction, copy=True)
    cumsum = future.cumsum()
    prediction_future = future.add(ts_log.ix[-1])
    prediction_future = prediction_future.add(cumsum)
    ts_future = np.exp(prediction_future)

    return ts_future


# Find outliers via the Tukey method. As defined in the README.md
class ARIMAHandler(Handler):
    class state(object):
        def __init__(self):
            self._times = []
            self._values = []

        def reset(self):
            self._times = []
            self._values = []

        def update(self, time, value):
            self._times.append(pd.datetime.fromtimestamp(time / 1e9))
            self._values.append(value)

        def to_series(self):
            df = pd.DataFrame({
                'Time': self._times,
                'Value': self._values
                })

            return df.set_index('Time')


    def __init__(self, agent):
        self._agent = agent
        self._state = ARIMAHandler.state()
        self._field = None
        self._forecast = None
        self._as = None
        self._begin_response = None


    def info(self):
        response = udf_pb2.Response()
        response.info.wants = udf_pb2.BATCH
        response.info.provides = udf_pb2.BATCH
        response.info.options['field'].valueTypes.append(udf_pb2.STRING)
        response.info.options['forecast'].valueTypes.append(udf_pb2.INT)
        response.info.options['as'].valueTypes.append(udf_pb2.STRING)

        logger.info("info")
        return response

    def init(self, init_req):
        success = True
        msg = ''
        for opt in init_req.options:
            if opt.name == 'field':
                self._field = opt.values[0].stringValue
            elif opt.name == 'forecast':
                self._forecast = opt.values[0].intValue
            elif opt.name == 'as':
                self._as = opt.values[0].stringValue

        if self._field is None:
            success = False
            msg += ' must supply field name'
        if self._forecast < 1:
            success = False
            msg += ' invalid scale must be >= 1'

        response = udf_pb2.Response()
        response.init.success = success
        response.init.error = msg[1:]

        return response

    def snapshot(self):
        response = udf_pb2.Response()
        response.snapshot.snapshot = ''

        return response

    def restore(self, restore_req):
        response = udf_pb2.Response()
        response.restore.success = False
        response.restore.error = 'not implemented'

        return response

    def begin_batch(self, begin_req):
        self._state.reset()

        # Keep copy of begin_batch
        response = udf_pb2.Response()
        response.begin.CopyFrom(begin_req)
        self._begin_response = response

    def point(self, point):
        logger.info(point)
        timestamp = point.time
        value = point.fieldsDouble[self._field]
        logger.info(value)
        logger.info(timestamp)
        self._state.update(timestamp, value)

    def end_batch(self, end_req):
        # Get predictions
        predictions = arima(self._state.to_series(), self._forecast)

        # Send begin batch with count of predictions
        self._begin_response.begin.size = len(predictions)
        self._agent.write_response(self._begin_response)

        response = udf_pb2.Response()
        for t, v in predictions.iterkv():
            point = udf_pb2.Point()
             #= time.mktime(t.timetuple())
            #point.time = int(timestamp * 1e9)
            print(v)
            point.time = 10
            point.name = self._field
            point.fieldsDouble[self._as] = v

            response.point.CopyFrom(point)
            self._agent.write_response(response)


        # Send an identical end batch back to Kapacitor
        response.end.CopyFrom(end_req)
        self._agent.write_response(response)


if __name__ == '__main__':
    a = Agent()
    h = ARIMAHandler(a)
    a.handler = h

    logger.info("Starting Agent")
    a.start()
    a.wait()
    logger.info("Agent finished")
