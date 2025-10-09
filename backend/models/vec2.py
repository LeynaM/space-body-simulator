from pydantic import BaseModel


class Vec2(BaseModel):
    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        if not isinstance(other, Vec2):
            return NotImplemented
        return Vec2(x=self.x + other.x, y=self.y + other.y)
