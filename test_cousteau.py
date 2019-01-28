import json
import datetime
import calendar
import json
import logging
from datetime import timedelta
from requests_futures.sessions import FuturesSession
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor

#IMPORT KAFKA PRODUCER
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='Kafka0:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
#end import
logging.basicConfig()#should be removable soon


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
    max_workers=4,
):
    """ Retry if there is a problem"""
    session = session or FuturesSession(max_workers=max_workers)
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def worker_task(sess, resp):
    """Process json in background"""
    try:
        resp.data = resp.json()
    except json.decoder.JSONDecodeError:
        logging.error("Error while reading Atlas json data.\n")
        resp.data = {}


def cousteau_on_steroid(params, retry=3):
    url = "https://atlas.ripe.net/api/v2/measurements/{0}/results"
    req_param = {
            "start": int(calendar.timegm(params["start"].timetuple())),
            "stop": int(calendar.timegm(params["stop"].timetuple())),
            }

    if params["probe_ids"]:
        req_param["probe_ids"] = params["probe_ids"]

    queries = []

    session = requests_retry_session()
    for msm in params["msm_id"]:
        queries.append( session.get(url=url.format(msm), params=req_param,
                        background_callback=worker_task
            ) )

    for query in queries:
        resp = query.result()
        yield (resp.ok, resp.data)



CollectionTime = datetime.datetime.utcnow()

while True:
    params = { "msm_id": [5001,5005, 5009, 5010, 5011, 5013, 5004], "start": (CollectionTime - timedelta(minutes=20)), "stop": (CollectionTime - timedelta(minutes=10)), "probe_ids": [] }
    for is_success, data in cousteau_on_steroid(params):

        if is_success:
            producer.send('TEST: THE SEQUEL', value=data)
            producer.flush()
        else:
            print("Error could not load the data")
    CollectionTime = CollectionTime + timedelta(minutes = 10)
    time.sleep(600)
