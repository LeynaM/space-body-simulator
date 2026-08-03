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

                    # conserve momentum
                    new_velocity = (
                        a.velocity.scalar_mult(a.mass) + b.velocity.scalar_mult(b.mass)
                    ).scalar_mult(1 / total_mass)

                    # mass-weighted position (optional)
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

        # remove merged bodies
        for index in sorted(to_remove, reverse=True):
            del bodies[index]


async def tick():
    dt = 0.01
    while True:
        for i in range(len(bodies)):
            for j in range(len(bodies)):
                if i != j:
                    bodies[i].applyForce(bodies[j])
            bodies[i].update(dt)
        merge_close_bodies(bodies)

        await asyncio.sleep(0.02)


@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(tick())
