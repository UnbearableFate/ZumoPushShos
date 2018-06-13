from Vector2 import *
import heapq
closed = dict()
opened = []
heapq.heapify(opened)

ROT_ANGLE = 90

ALL_DISTANCE = 0
ALL_ANGEL =0

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

'''
def pointInPolygon(p, ptPolygon, nCount) :
    nCross =0
    for i in range(0,nCount) :
        p1 = ptPolygon[i]
        p2 = ptPolygon[(i+1)%nCount]
        if abs(p1.y - p2.y) < ALMOST_ZERO :
            continue
        if p.y < min(p1.y,p2.y) :
            continue
        if p.y >= max(p1.y,p2.y) :
            continue

        xx = (p.y-p1.y) *(p2.x-p1.x) /(p2.y-p1.y) +p1.x
        if xx > p.x:
            ++nCross

    return nCross%2 == 1
'''


class state :

    def __init__(self):
        self.parent = 0
        self.position = Vector2(0,0)
        self.rotation = Vector2(0,0)
        self.rotateAngle = 0
        self.forward = 1
        self.f = 0
        self.h = 0
        self.hash = ""

    def __init__(self,position,rotation, parent,goal_position,goal_rotation,forw = 1):
        self.parent = parent
        self.position = position
        self.rotation = rotation.normalization()
        self.rotateAngle = 0
        if parent != 0:
            ff = (position - parent.position).magnitude() * DISTANCE_WEIGHT
            ff2 = abs(parent.rotation.get_angle(rotation))* ANGLE_WEIGHT *1.5
            self.f = ff + ff2
        else:
            self.f = 0
        ang = goal_rotation.get_angle(self.rotation)
        if ang > PI:
            ang = 2 * PI - ang
        #self.h = (abs(goal_position.x - self.position.x) + abs(goal_position.y - self.position.y))*DISTANCE_WEIGHT + abs(ang) * ANGLE_WEIGHT
        self.forward = forw
        self.h = (goal_position - self.position).magnitude() * DISTANCE_WEIGHT
        self.h += ang * ANGLE_WEIGHT
        self.hash = truncate(self.position.x,PRECISION) +","+truncate(self.position.y,PRECISION)+","+truncate(self.rotation.x,PRECISION)+","+truncate(self.rotation.y,PRECISION)+","+str(self.forward)

    def __lt__(self, other):
        return self.f + self.h < other.f + other.h

    def __eq__(self, other):
        res = False
        if isinstance(other,state):
            res = ( self.position == other.position and self.rotation == other.rotation )
        else:
            return False

    def getRoute(self):
        p = self
        res = []
        while p !=0:
            if isinstance(p, state) :
                leftSpeed = (SPEED * DeltaT - ZUMO_WHEELDISTANCE * math.sin(p.rotateAngle)) / DeltaT
                rightSpeed = (SPEED * DeltaT + ZUMO_WHEELDISTANCE * math.sin(p.rotateAngle)) /DeltaT
                res.insert(0, [p.position,p.rotation,p.rotateAngle,p.forward,leftSpeed,rightSpeed])
                p = p.parent
            else:
                break

        return res

    def getHash(self):
        return self.hash



'''
def distance_point_line(point1, point2,point) :
    A = point2.y - point1.y
    B = point1.x - point2.x
    C = point2.x * point1.y - point1.x * point2.y
    up = abs(A * point.x + B* point.y + C)
    down = math.sqrt(A *A + B*B)
    return  up / down
'''

def FindRoute(start_pos, start_rot,goal_pos, goal_rot,obstacle_list):
    opened.clear()
    closed.clear()
    ALL_DISTANCE = (goal_pos - start_pos).magnitude()
    ALL_ANGEL = start_rot.get_angle(goal_rot)
    first_state = state(start_pos,start_rot,0,goal_pos,goal_rot)
    heapq.heappush(opened,first_state)
    while(True) :
        current_state = heapq.heappop(opened)
        print(current_state.h + current_state.f)
        if current_state.position == goal_pos and current_state.rotation == goal_rot :
            return current_state.getRoute()

        if current_state.position == goal_pos :
            rott = current_state.rotation.get_angle(goal_rot)
            if not (current_state.rotation.rotate(rott) == goal_rot) :
                rott = -rott
            childstate = state(current_state.position,goal_rot,current_state,goal_pos,goal_rot)
            childstate.rotateAngle = rott
            return childstate.getRoute()

        ##rr = int(360 / ROT_ANGLE)
        rr1 = int(-180 / ROT_ANGLE)
        rr2 = int(180 / ROT_ANGLE)
        possbilePoint = 0
        for i in range(rr1 ,rr2) :
            angle = i * PI * ROT_ANGLE / 180
            radius = math.sqrt(ZUMO_WIDTH * ZUMO_WIDTH / 4 + (ONE + ZUMO_LENGTH / 2) * (ONE + ZUMO_LENGTH / 2))
            point1 = current_state.position + current_state.rotation.rotate(angle + PI * ROT_ANGLE / 360).norm_mul(radius)
            point2 = current_state.position + current_state.rotation.rotate(angle - PI * ROT_ANGLE / 360).norm_mul(radius)

            okchild = True

            for oo in obstacle_list :
                if lineWithPolygon(point1,point2,oo):
                    okchild = False
                    break
                if compl_inside_convex(point1,oo) or compl_inside_convex(point2,oo) :
                    okchild = False

            if okchild :
                newpos = current_state.position + current_state.rotation.rotate(angle)* ONE
                newrot = current_state.rotation.rotate(angle).normalization()

                childstate = state(newpos, newrot, current_state, goal_pos, goal_rot)
                if angle > PI :
                    aa = angle - 2 * PI
                else:
                    aa = angle

                childstate.rotateAngle = aa
                ++possbilePoint

                if not childstate.getHash() in closed:
                    closed[childstate.getHash()] = []
                    heapq.heappush(opened, childstate)
                else:
                    findChild = False
                    for oldstate in closed[childstate.getHash()]:
                        if oldstate == childstate:
                            findChild = True

                    if not findChild:
                        heapq.heappush(opened, childstate)

        if possbilePoint == 0 and len(opened) == 0:
            newpos = current_state.position + current_state.rotation * -1 * ONE
            childstate = state(newpos, current_state.rotation,current_state,goal_pos,goal_rot,-1)
            if not childstate.getHash() in closed:
                closed[childstate.getHash()] = []
                heapq.heappush(opened, childstate)
            else:
                findChild = False
                for oldstate in closed[childstate.getHash()]:
                    if oldstate == childstate:
                        findChild = True

                if not findChild:
                    heapq.heappush(opened, childstate)


        if not current_state.getHash() in closed:
            closed[current_state.hash] = []

        closed[current_state.hash].append(current_state)












