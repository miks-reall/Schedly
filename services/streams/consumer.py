'''

Event-driven handler writen without AI.
Part 2. Consumer that listens a stream and ready to read stream.

'''

''' Imports '''
from time import sleep
from redis import StrictRedis
from random import randint as rand
from redis.exceptions import TimeoutError
from redis_streams.consumer import Consumer, RedisMsg
from services.streams.common import REDIS_HOST, REDIS_PASS, REDIS_PORT, STREAM, GROUP, REDIS_USER


''' Run main code '''
if __name__ == "__main__":
    try:
        consumer = Consumer(
            redis_conn=StrictRedis(
                decode_responses=True,
                username=REDIS_USER,
                password=REDIS_PASS,
                host=REDIS_HOST,
                port=REDIS_PORT
            ),
            stream=STREAM,
            consumer_group=GROUP,
            batch_size=3,
            max_wait_time_ms=30000
        )
        print("Consumer init succesfull")
        while True:
            messages = consumer.get_items()
            for i, item in enumerate(messages):
                print(f"Pocessing {i+1}/{len(messages)} message:{item}")
                consumer.remove_item_from_consumer_group(item_id=item.msgid)
    except KeyboardInterrupt:
        print("Consumer finished")
    except TimeoutError:
        print("TimeoutError")
        