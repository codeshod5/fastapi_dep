from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer, errors as kafka_errors,KafkaConsumer
from pydantic import BaseModel
import json
import time

from contextlib import asynccontextmanager

class LoginInfo(BaseModel):
    username: str
    phone: int
    area: str
    long: str
    lat: str
    status:str
# #     bus_id: 
# class customnotify(BaseModel):
#     cus_id:int
#     route_id:int
#     bus_id:int
#     phone:int
class send_by_driver(BaseModel):
    bus_id:int
    route_id:int
    area:str


    



async def create_producer_with_retry(
    bootstrap_servers: str, 
    retries: int = 5, 
    backoff: float = 2.0
) -> KafkaProducer:
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
           
            return KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                api_version=(0, 10, 2),
                key_serializer=lambda k: json.dumps(k).encode('utf-8'),  
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except kafka_errors.NoBrokersAvailable as e:
            last_exc = e
            print(f"[producer] attempt {attempt} failed, retrying in {backoff}s…")
            time.sleep(backoff)
    raise last_exc

@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = await create_producer_with_retry("kafka:9092", retries=10, backoff=3)
    app.state.kafka_producer = producer
    yield
    producer.close()

app = FastAPI(lifespan=lifespan)

# @app.post("/message")
# async def send_login(log: LoginInfo):
#     try:
#         app.state.kafka_producer.send("login_logs", log.dict())
#         return {"message": "Sent to Kafka"}
#     except Exception as exc:
#         # unexpected failure—return 503 so the client can retry
#         raise HTTPException(status_code=503, detail=str(exc))
    
@app.post("/update")
async def send_update_of_location(loc: send_by_driver):
    try:
        # data = {"bus_id": loc.bus_id, "route_id": loc.route_id}

        producer = app.state.kafka_producer

        producer.send(
            "send_notification",
            key=loc.route_id,  
            value=loc.dict() 
        )
        producer.flush()
        return {"status": "Message sent"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))




    




# app/main.py
# app/main.py
# app/main.py
# import json
# from contextlib import asynccontextmanager

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from aiokafka import AIOKafkaProducer

# class LoginInfo(BaseModel):
#     username: str
#     phone: int
#     area: str

# producer: AIOKafkaProducer | None = None

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     global producer
#     producer = AIOKafkaProducer(
#         bootstrap_servers="kafka:9092",
#         value_serializer=lambda v: json.dumps(v).encode(),
#     )
#     await producer.start()      # now guaranteed to succeed
#     yield
#     await producer.stop()

# app = FastAPI(lifespan=lifespan)

# @app.post("/message")
# async def send_message(log: LoginInfo):
#     try:
#         await producer.send_and_wait("login_logs", log.dict())
#         return {"message": "Sent to Kafka"}
#     except Exception as e:
#         raise HTTPException(status_code=503, detail=str(e))








