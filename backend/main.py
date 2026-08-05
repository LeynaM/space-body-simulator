import asyncio
import json
import time

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
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

MAX_BODIES = 80

MAX_DT = 0.05

bodies = []
connections = set()
tick_task = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/bodies")
def read_bodies():
    return bodies


@app.post("/bodies")
def create_body(body: Body):
    if len(bodies) >= MAX_BODIES:
        raise HTTPException(
            status_code=429,
            detail=f"The simulation is full ({MAX_BODIES} bodies).",
        )

    bodies.append(body)
    return body


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    add_viewer(websocket)
    try:
        while True:
            data = json.dumps(jsonable_encoder(bodies))
            await websocket.send_text(data)
            await asyncio.sleep(0.2)
    except (WebSocketDisconnect, RuntimeError):
        pass
    finally:
        remove_viewer(websocket)


def add_viewer(websocket):
    global tick_task

    connections.add(websocket)
    if tick_task is None:
        tick_task = asyncio.create_task(tick())


def remove_viewer(websocket):
    global tick_task

    connections.discard(websocket)
    if connections:
        return

    if tick_task is not None:
        tick_task.cancel()
        tick_task = None
    bodies.clear()


def merge_close_bodies(bodies):
    merged = True
    while merged:
        merged = False
        to_remove = set()

        for i in range(len(bodies)):
            if i in to_remove:
                continue
            for j in range(i + 1, len(bodies)):
                if j in to_remove:
                    continue

                a = bodies[i]
                b = bodies[j]
                distance = (a.position - b.position).get_mag()

                if distance < 0.5 * (a.diameter + b.diameter):
                    total_mass = a.mass + b.mass

                    new_velocity = (
                        a.velocity.scalar_mult(a.mass) + b.velocity.scalar_mult(b.mass)
                    ).scalar_mult(1 / total_mass)

                    new_position = (
                        a.position.scalar_mult(a.mass) + b.position.scalar_mult(b.mass)
                    ).scalar_mult(1 / total_mass)

                    a.mass = total_mass
                    a.velocity = new_velocity
                    a.position = new_position
                    a.diameter = 2 * (
                        (a.diameter / 2) ** 3 + (b.diameter / 2) ** 3
                    ) ** (1 / 3)

                    to_remove.add(j)
                    merged = True
                    break

            if merged:
                break

        for index in sorted(to_remove, reverse=True):
            del bodies[index]


async def tick():
    last = time.monotonic()
    while True:
        await asyncio.sleep(0.02)

        now = time.monotonic()
        dt = min(now - last, MAX_DT)
        last = now

        for i in range(len(bodies)):
            for j in range(len(bodies)):
                if i != j:
                    bodies[i].applyForce(bodies[j])
            bodies[i].update(dt)
        merge_close_bodies(bodies)
