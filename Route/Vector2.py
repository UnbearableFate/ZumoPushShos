import  math
ONE = 1
PI = 3.14
DISTANCE_WEIGHT = 1
ANGLE_WEIGHT =  2 * ONE /PI * 0.2
PRECISION = 2

ZUMO_LENGTH = 10.2
ZUMO_WIDTH = 10
ZUMO_WHEELDISTANCE = 8.7
SHOES_LENGTH = 28
SHOES_WIDTH = 10
ALMOST_ZERO = 0.1
MAX_VALUE = 100

DeltaT = 0.05
SPEED = 19
ZUMOVVSREALV = 5

MAX_ROTATE = PI / 6


class Vector2 :
    def __init__(self, x, y):
        self.x = x
        self.y = y
        '''
        if isinstance(x, list):
            self.x = x
            self.y = y
        else:
            self.x = x
            self.y = y
        '''
    def __mul__(self, other):
        if isinstance(other,Vector2):
            return self.x * other.x + self.y * other.y
        return Vector2(other * self.x, other * self.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x-other.x, self.y - other.y)

    def __eq__(self, other):
        if (self - other).magnitude() < ALMOST_ZERO*10 :
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

def degToArc(deg):
    return deg / 180.0 * PI
def arcToDeg(arc):
    return arc / PI * 180.0

def getSign(a) :
    if a < 0:
        return -1
    else:
        return  1

def makeN(a, n = 3) :
    a = int(a)
    res = ""
    if a >= 0 :
        res += "+"
    else:
        res += "-"

    if abs(a) < 10 :
        res += "00"+str(abs(a))
    if abs(a) >= 10 and abs(a) < 100 :
        res += "0"+str(abs(a))
    if abs(a) >= 100 :
        res += str(abs(a))
    return res

def makeFour(a) :
    a = int(a)
    res = ""
    if abs(a) < 10:
        res += "000" + str(abs(a))
    if abs(a) >= 10 and abs(a) < 100:
        res += "00" + str(abs(a))
    if abs(a) >= 100 and abs(a) < 1000:
        res += "0" + str(abs(a))
    if abs(a) >= 1000:
        res += str(abs(a))
    return res


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def cross(p0,p1,p2) :
    return (p1.x- p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y)

def min(a,b) :
    if a < b :
        return a
    else:
        return b

def max(a,b) :
    if a > b :
        return a
    else:
        return b

def compl_inside_convex (target,polygon) : #point in polygon
    n = len(polygon)
    if len(polygon) <3 :
        return  False
    if cross(polygon[0],target,polygon[1]) > -1*ALMOST_ZERO :
        return False
    if cross(polygon[0],target, polygon[n-1]) < ALMOST_ZERO :
        return False

    i = 2
    j = n-1
    line = -1
    while i <= j :
        mid = int((i+j)/2)
        if cross(polygon[0],target,polygon[mid]) :
            line = mid
            j = mid -1
        else:
            i = mid +1

    return cross(polygon[line -1],target,polygon[line]) > -ALMOST_ZERO

def lineIntersect(ap1,ap2,bp1,bp2):
    nap1 = Vector2(0,0)
    nap2 = ap2 + ap1 * -1
    nbp1 = bp1 + ap1 * -1
    nbp2 = bp2 + ap1 * -1

    rotA = nap2.get_angle(Vector2(1,0))
    if abs(nap2.rotate(rotA).y) < ALMOST_ZERO :
        nap2 = nap2.rotate(rotA)
    else:
        rotA *= -1
        nap2 = nap2.rotate(rotA)

    nbp1 = nbp1.rotate(rotA)
    nbp2 = nbp2.rotate(rotA)

    if nbp2.y * nbp1.y > 0 :
        return False

    '''
    A0 = nap1.y - nap2.y
    B0 = nap2.x - nap1.x
    C0 = nap1.x * nap2.y - nap2.x * nap1.y

    A1 = nbp1.y - nbp2.y
    B1 = nbp2.x - nbp1.x
    C1 = nbp1.x * nbp2.y - nbp2.x * nbp1.y

    D = A0 * B1 -A1 *B0
    if D == 0 :
        return  True
    else:
        x = 
    '''
    A1 = nbp1.y - nbp2.y
    B1 = nbp2.x - nbp1.x
    C1 = nbp1.x * nbp2.y - nbp2.x * nbp1.y
    if A1 == 0 :
        return True

    xx = -1 * C1 / A1
    if xx < 0 :
        return False
    elif xx > nap2.x :
        return False
    else:
        return True

def lineWithPolygon(p1,p2,polygon) :
    for i in range (0, len(polygon)) :
        pp1 = polygon[i]
        pp2 = polygon[(i+1)%len(polygon)]
        if lineIntersect(p1,p2,pp1,pp2) :
            return True
    return False

def intersection(p0,v0,p1,v1):
    m = v0.x*(p1.y - p0.y) - v0.y *(p1.x- p0.x)
    n = v1.x * v0.y - v0.x * v1.y
    if abs(n) < 0.0001 :
        return (p0 + p1) * 0.5
    m = m / n
    interPoint = p1 + v1 * m
    return interPoint

def leftOrRight(p1,v1,p2):
    temp = p2 - p1
    arc = v1.get_angle(Vector2(1,0))
    if v1.y > 0 :
        temp = temp.rotate(-arc)
    else:
        temp = temp.rotate(arc- 2*PI)

    if temp.y > 0.00001 :
        return 1
    if temp.y < -0.00001 :
        return -1
    else:
        return 0



