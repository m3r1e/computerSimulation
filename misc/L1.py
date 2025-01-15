import math

class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v):
        new_x = self.x + v.x
        new_y = self.y + v.y
        new_v = Vec2D(new_x, new_y)
        return new_v
    
    def inplace_add(self, v):
        self.x += v.x
        self.y += v.y

    @classmethod
    def add_vecs(cls, a, b):
        new_x = a.x + b.x
        new_y = a.y + b.y
        v = cls(new_x, new_y)
        return v
    
    def magnitude(self):
        mag = math.sqrt(self.x*self.x + self.y*self.y)
        return mag

    def __str__(self):
        return f"({self.x}, {self.y})"

def main():
    v1 = Vec2D(3.0, 4.0)
    v2 = Vec2D(2.0, -1.0)

    v1.inplace_add(v2)
    print(v1)

    v3 = v1.add(v2)
    print(v3)

    v4 = Vec2D.add_vecs(v2, v3)
    print(v4)

if __name__ == "__main__":
    main()