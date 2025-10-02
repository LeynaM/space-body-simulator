import asyncio
import json

from fastapi import FastAPI, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


class Vec2(BaseModel):
    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        if not isinstance(other, Vec2):
            return NotImplemented
        return Vec2(x=self.x + other.x, y=self.y + other.y)


class Body(BaseModel):
    position: Vec2
    velocity: Vec2


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
        print("sending", data)
        await asyncio.sleep(1)


async def tick():
    while True:
        for body in bodies:
            body.position += body.velocity
        await asyncio.sleep(1)


@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(tick())
