import apsw
import multiprocessing
import logging
import json
from kafka import KafkaProducer
import traceback


class Saver(multiprocessing.Process):
    """Dumps data to a SQLite database. """

    def __init__(self, filename, saver_queue):
        multiprocessing.Process.__init__(self)
        logging.warn("Init saver")
        self.producer = None
        self.saver_queue = saver_queue
        self.expid = None
        self.prevts = -1
        logging.warn("End init saver")

    def run(self):

        logging.info("Started saver")
        self.producer = KafkaProducer(bootstrap_servers=['Kafka0:9092', 'Kafka1:9092', 'Kafka2:9092'],
                                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        main_running = True

        while main_running or not self.saver_queue.empty():
            elem = self.saver_queue.get()
            if isinstance(elem, str):
                if elem.endswith(";"):
                    pass
                elif elem == "MAIN_FINISHED":
                    main_running = False
            else:
                self.save(elem)
            # self.saver_queue.task_done()

    def save(self, elem):

        t, data = elem

        if t == "diffrtt":
            (ts, startpoint, endpoint, median, minimum, nb_samples, nb_tracks,
                    nb_probes, entropy, hop, nbrealrtts) = data

            serialized_data = {
                'ts' : ts,
                'startpoint' : startpoint,
                'endpoint' : endpoint,
                'median' : median,
                'minimum' : minimum,
                'nb_samples' : nb_samples,
                'nb_tracks' : nb_tracks,
                'nb_probes' : nb_probes,
                'entropy' : entropy,
                'hop' : hop,
                'nbrealrtts' : nbrealrtts
                }


            self.producer.send('newsaver', value = serialized_data)
            if self.prevts != ts:
                self.prevts = ts
                self.producer.flush()
                logging.info("start recording diff. RTTs (ts={})".format(ts))
