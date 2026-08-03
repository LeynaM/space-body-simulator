import math

from pydantic import BaseModel


class Vec2(BaseModel):
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: "Vec2") -> "Vec2":
        if not isinstance(other, Vec2):
            return NotImplemented
        return Vec2(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        if not isinstance(other, Vec2):
            return NotImplemented
        return Vec2(x=self.x - other.x, y=self.y - other.y)

    def scalar_mult(self, value: float) -> "Vec2":
        return Vec2(x=self.x * value, y=self.y * value)

    def get_mag(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def get_unit(self) -> "Vec2":
        return self.scalar_mult(1 / self.get_mag())

    def set_mag(self, mag: float) -> None:
        temp_vec = self.get_unit().scalar_mult(mag)
        self.x = temp_vec.x
        self.y = temp_vec.y
