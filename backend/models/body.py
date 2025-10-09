from pydantic import BaseModel

from models.vec2 import Vec2


class Body(BaseModel):
    position: Vec2
    velocity: Vec2

    def update(self):
        self.position += self.velocity
