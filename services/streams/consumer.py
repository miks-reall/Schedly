'''

Event-driven handler writen without AI.
Part 2. Consumer that listens a stream and ready to read stream.

'''

''' Imports '''
from time import sleep
from redis import StrictRedis
from random import randint as rand
from redis_streams.consumer import Consumer
from services.streams.common import REDIS_HOST, REDIS_PASS, REDIS_PORT, STREAM, GROUP

''' Initials '''
redis_conn = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True, ssl=True, ssl_cert_reqs=None)
consumer = Consumer(redis_conn=redis_conn, stream=STREAM, consumer_group=GROUP, batch_size=10, max_wait_time_ms=30000)

''' Run main code '''
if __name__ == "__main__":
    pass