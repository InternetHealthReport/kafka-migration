import json
import datetime
import calendar
import logging
import itertools
import threading
import json
# from ripe.atlas.cousteau import AtlasResultsRequest
from progress.bar import Bar
from kafka import KafkaConsumer, KafkaProducer



class Reader():

    def __init__(self, start, end, timetrack_converter, msm_ids=[5001,5004,5005],
            probe_ids=[1,2,3,4,5,6,7,8], chunk_size=900):


        # self.semaphore = None
        self.msm_ids = msm_ids
        self.probe_ids = probe_ids
        self.start = start
        self.end = end
        self.chunk_size = chunk_size
        self.params = []
        self.timetrack_converter = timetrack_converter
        #self.bar = None
        self.consumer = None


    def __enter__(self):

        self.consumer = KafkaConsumer(bootstrap_servers=[ 'Kafka1:9092', 'Kafka2:9092'],
                                         auto_offset_reset='earliest',
                                         value_deserializer=lambda m: json.loads(m),
                                         group_id='blah',
                                         consumer_timeout_ms=10000)
        self.consumer.subscribe('ATLAS_TEST_5')
        return self

    def __exit__(self, type, value, traceback):
        self.close()


    def read(self):
        emptyCount = 0;
        #self.bar = Bar("Processing", max=len(self.params), suffix='%(percent)d%%')
        logging.info("Entering Infinite For")
        for message in self.consumer:
            traceroute = message.value
            yield self.timetrack_converter.traceroute2timetrack(traceroute)
            pass
        self.consumer.close()
        logging.info("should be closed")




    def close(self):
        #self.bar.finish()
        return False


if __name__ == "__main__":
    with atlasrestreader(datetime.datetime(2018,6,1,0,0), datetime.datetime(2018,6,2,0,0)) as arr:
            for tr in arr:
                print(tr)
