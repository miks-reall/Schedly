'''

Event-driven handler writen without AI.
Part 1. Producer that publishes events to a stream once a 3-10 seconds.

'''

''' Imports '''
from time import sleep
from redis import StrictRedis
from random import randint as rand
from redis_streams.producer import Producer
from services.streams.common import REDIS_HOST, REDIS_PASS, REDIS_PORT, STREAM, REDIS_USER

''' Initials '''
redis_conn = StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASS,
    username=REDIS_USER,
)
producer = Producer(redis_conn=redis_conn, stream=STREAM) 

''' Functions '''

def wait_random_time() -> int:
    time = rand(3,10)
    sleep(time)
    return time

''' Run main code '''
if __name__=="__main__":
    
    ''' Publish message to stream '''
    try:
        for itteration in range(100):
            ''' Publish messages to Stream for 100 times with random delay'''
            msg_id = producer.add({"message":f"Hello, {itteration} times", "itteration":itteration})
            print(f"Published {msg_id} for {itteration} time(s)")
            print("Waiting...")
            time = wait_random_time()
            print(f'{time} seconds have passed')
    except KeyboardInterrupt:
        ''' If I want to exit '''
        print('\nProcess was finished with code 0')
    



