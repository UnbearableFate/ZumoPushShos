import  math

ONE = 0.1
PI = 3.14
DISTANCE_WEIGHT = 1
ANGLE_WEIGHT =  2 * ONE /PI * 0.8
PRECISION = 2

ZUMO_LENGTH = 0.6
ZUMO_WIDTH = 0.6
ZUMO_WHEELDISTANCE = 0.4
SHOES_LENGTH = 0.8
SHOES_WIDTH = 0.6
ALMOST_ZERO = 0.01
MAX_VALUE = 200

DeltaT = 0.01
SPEED = 1


class Vector2 :
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if isinstance(other,Vector2):
            return self.x * other.x + self.y * other.y
        return Vector2(other * self.x, other * self.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x-other.x, self.y - other.y)

    def __eq__(self, other):
        if (self - other).magnitude() < ALMOST_ZERO :
            return True
        if self.get_angle(other) < ALMOST_ZERO * 2 :
            return True
        return False

    def __str__(self):
        return ("["+str(self.x)+" , "+str(self.y)+"]")

    def norm_mul(self,a):
        return Vector2(a * self.x, a * self.y)

    def normalization(self):
        self = self.norm_mul(1.0 / self.magnitude())
        return self

    def rotate(self,angle):
        xx = math.cos(angle) * self.x - math.sin(angle) * self.y
        yy = math.sin(angle) * self.x + math.cos(angle) * self.y
        return Vector2(xx, yy)

    def magnitude(self):
        return math.sqrt(self * self)

    def panning(self,x,y):
        return self + Vector2(x,y)

    def get_angle(self, vec):
        d = self * vec
        ma = self.magnitude() * vec.magnitude()
        if ma == 0 :
            return 2 *PI
        rr = d / ma
        if rr > 1 :
            rr = 1
        if rr < -1 :
            rr = -1
        return math.acos(rr)

