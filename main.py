from fastapi import FastAPI, Request
from fastapi.middleware.cors    import CORSMiddleware
from redis_om   import get_redis_connection, HashModel

from env    import Environment as env
# from fastapi.websockets import WebSocket
 
# fastapi config 
app = FastAPI()
origins = [""]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)


# redis connection 
redis = get_redis_connection(host=env.redis_host,
                             port=env.redis_port,
                             decode_responses=True)

# models
class Delivery(HashModel):
    cost:int = 0
    notes:str = ''

    class Meta:
        database = redis

class Event(HashModel):
    delivery_id:str|None
    type:str
    data:str

    class Meta:
        database = redis


# endpoints
@app.get("/")
async def read_main():
    return {"msg": "redis study"}

@app.post(path='/delivery/create')
async def create(request: Request):
    body = await request.json()
    delivery  = Delivery(cost=body['data']['cost'],
                         notes=body['data']['notes']).save()     # 'data' = default key
    return delivery



# @app.websocket("/ws")
# async def websocket(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_json({"msg": "Hello WebSocket"})
#     await websocket.close()

