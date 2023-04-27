from fastapi import FastAPI , WebSocket, WebSocketDisconnect
from typing import List
import time
import threading
import asyncio
import uvicorn
import aioredis

app = FastAPI()
@app.get('/')
def hello():
    return {
        'message': 'fastapi is working'
    }
 
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.redis = aioredis.from_url("redis://127.0.0.1",encoding="utf-8",decode_responses = True)
        self.existedConnection = False

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        if self.existedConnection == False:
            self.existedConnection = True
            await self.runRedisJob()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if len(self.active_connections)==0:
            self.existedConnection = False

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def message2redis(self , message:str):
        await self.redis.publish("chat:c", message)

    async def runRedisJob(self):
        async def listenRedis():
            pubsub = self.redis.pubsub()
            await pubsub.psubscribe("chat:c")
            while self.existedConnection:
                message = await pubsub.get_message()
                if message:
                    await self.broadcast(str(message['data']))
                time.sleep(0.5)

        t = threading.Thread(target=asyncio.run, args=(listenRedis(),))
        t.start()

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.message2redis(data)
            await manager.send_personal_message(f"You wrote: {data}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

async def get_redis_pool():
    redis = await aioredis.from_url("redis://127.0.0.1",encoding="utf-8",decode_responses = True)
    try:
        result = await redis.ping()
    except:
        raise SystemError('redis is not serving!')

# -- confirm redis is working --
@app.on_event("startup")
async def startup_event():
    await get_redis_pool()

if __name__ == '__main__':
    uvicorn.run(app , host = "127.0.0.1" , port = 8000 , workers=4)

# if you dont have pipenv 
# pip install pipenv
# pipenv shell
# pipenv install (install package in pipfile)
# pipenv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4