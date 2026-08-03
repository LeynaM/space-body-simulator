from pydantic import BaseModel

from models.vec2 import Vec2


class Body(BaseModel):
    diameter: float = 40
    position: Vec2
    velocity: Vec2 = Vec2()
    force: Vec2 = Vec2()
    mass: float = 6 * pow(10, 4)

    def update(self, dt=0.01):
        acceleration = self.force.scalar_mult(1 / self.mass)
        self.velocity += acceleration.scalar_mult(dt)
        self.position += self.velocity.scalar_mult(dt)
        self.force = Vec2()

    def applyForce(self, body: "Body"):
        force = body.position - self.position
        distance = force.get_mag()
        distance = max(distance, 10)
        gravitational_constant = 6.67 * pow(10, -1)
        strength = (gravitational_constant * (self.mass * body.mass)) / (
            distance * distance
        )
        force.set_mag(strength)
        self.force += force
