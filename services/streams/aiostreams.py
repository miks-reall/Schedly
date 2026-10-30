'''

Async API for Redis Streams

'''

''' Imports '''
from os import getpid
from typing import Any
from socket import gethostname
import redis.asyncio as aioredis
from dataclasses import dataclass
from redis.exceptions import ResponseError, TimeoutError


'''  Redis Messages class for simplified data storage '''
@dataclass
class RedisMsg:
    msg_id: str
    data: dict[str, Any]

''' Producer (that who puts data into a stream) class '''
class Producer:
    def __init__(self, redis_conn: aioredis.Redis, stream: str):
        self.redis = redis_conn
        self.stream = stream
    
    async def add(self, data:dict[str, Any] ) -> str:
        return await self.redis.xadd(name=self.stream, fields=data)

''' Consumer (that who read data from a stream) class '''
class Consumer:
    def __init__(
        self,
        redis_conn: aioredis.Redis,
        stream: str,
        consumer_group: str,
        batch_size: int = 10,
        timeout_ms: int = 30000,
        consumer_name: str | None = None
    ):
        self.redis = redis_conn
        self.stream = stream
        self.group = consumer_group
        self.batch_size = batch_size
        self.timeout = timeout_ms

        self.consumer_name = consumer_name or f"{gethostname()}-{getpid()}"
        self._group_checked = False
    
    ''' check the group has been created '''
    async def _ensure_group(self) -> None:
        
        if self._group_checked:
            return 
        
        try:
            await self.redis.xgroup_create(
                name=self.stream,
                groupname=self.group,
                id="0",
                mkstream=True
            )
        except ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise
        
        self._group_checked = True
    
    ''' return list of RedisMsg objects '''
    async def get_items(self) -> list[RedisMsg]:

        await self._ensure_group() # checking

        response = await self.redis.xreadgroup(
            groupname=self.group,
            consumer_name=self.consumer_name,
            streams={self.stream: ">"},
            count=self.batch_size,
            block=self.timeout
        )

        if not response:
            return []
        
        '''

        ------- Example of response --------

        [
        "BatchStream",  # Stream name
            [
                # List of messages (everyone is tuple)
                ("1730280000000-0", {"message": "Hello", "iteration": "0"}),
                ("1730280005000-0", {"message": "World", "iteration": "1"})
            ]
        ]

        '''

        items = []
        for _, message in response:
            for msg_id, fields in message:
                items.append(RedisMsg(msg_id=msg_id, fields=fields))
        return items
    
    ''' XACK item from stream and XDEL (Optional) '''
    async def ack_item(self, msg_id: str, delete_from_stream: bool = False) -> None:
        await self.redis.xack(self.stream, self.group, msg_id)
        if delete_from_stream:
            await self.redis.xdel(self.stream, msg_id)
