from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
bodies = []


class Position(BaseModel):
    x: float
    y: float


class Body(BaseModel):
    position: Position


@app.get("/bodies")
def read_bodies():
    return bodies


@app.post("/bodies")
def create_body(body: Body):
    bodies.append(body)
    return body
