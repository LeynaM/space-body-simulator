import asyncio
import json

from fastapi import FastAPI, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from models.body import Body

app = FastAPI()
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


bodies = []


@app.get("/bodies")
def read_bodies():
    return bodies


@app.post("/bodies")
def create_body(body: Body):
    bodies.append(body)
    return body


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = json.dumps(jsonable_encoder(bodies))
        await websocket.send_text(data)
        await asyncio.sleep(0.2)


async def tick():
    dt = 0.01
    while True:
        for i in range(len(bodies)):
            for j in range(len(bodies)):
                if i != j:
                    bodies[i].applyForce(bodies[j])
            bodies[i].update(dt)

        await asyncio.sleep(0.02)


@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(tick())
