'''

Event-driven handler based on Aioredis Streams API (writen by Me)

'''

''' Imports '''
import asyncio
import redis.asyncio as aioredis
from redis.exceptions import TimeoutError
from services.streams.aiostreams import RedisMsg, Consumer, Producer
from common import StreamName, GroupName, REDIS_HOST, REDIS_PASS, REDIS_PORT, REDIS_USER, ParserAct


''' Main function of handler '''
async def main() -> None:
    # connect to redis
    redis_conn = aioredis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        username=REDIS_USER,
        password=REDIS_PASS
    )
    
    # Create consumer for common stream
    consumer = Consumer(
        redis_conn=redis_conn,
        stream=StreamName.COMMON,
        consumer_group=GroupName.COMMON,
        timeout_ms=5000
    )

    ''' create producers for any streams '''
    vk_producer = Producer(redis_conn=redis_conn, stream=StreamName.VK)
    tg_producer = Producer(redis_conn=redis_conn, stream=StreamName.TG)

    ''' Infnite listenning '''
    while True:
        try:
            
            items = await consumer.get_items() # get non-ACK items from common stream

            ''' Wait if nothing '''
            if not items:
                asyncio.sleep(3)
                continue
            
            ''' Handler of messages '''
            for item in items:
                ''' Get all attachments from message '''
                process = item.data.get("process")
                action = item.data.get("action")
                args = item.data.get("args")
                
                ''' Sorting by process name '''
                if process == "parser":
                    ''' Method handlers from Parser process '''
                    if action == ParserAct.SCH_ADD:
                        vk_producer.add(data={"act":action, "args":args})
                        


        except TimeoutError:
            continue
