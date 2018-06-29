from Route.Vector2 import *
import heapq
closed = dict()
opened = []
heapq.heapify(opened)

ROT_ANGLE = 1

ALL_DISTANCE = 0
ALL_ANGEL =0


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
        self.rotateArc = 0
        self.forward = 1
        self.f = 0
        self.h = 0
        self.hash = ""

    def __init__(self,position,rotation, parent,goal_position,goal_rotation,forw = 1):
        self.parent = parent
        self.position = position
        self.rotation = rotation.normalization()
        self.rotateArc = 0
        if parent != 0:
            ff = (position - parent.position).magnitude() * DISTANCE_WEIGHT
            ff2 = abs(parent.rotation.get_angle(rotation))* ANGLE_WEIGHT
            self.f = ff + ff2
        else:
            self.f = 0
        ang = goal_rotation.get_angle(self.rotation)
        if ang > PI:
            ang = 2 * PI - ang
        #self.h = (abs(goal_position.x - self.position.x) + abs(goal_position.y - self.position.y))*DISTANCE_WEIGHT + abs(ang) * ANGLE_WEIGHT
        self.forward = forw
        self.h = (goal_position - self.position).magnitude() * DISTANCE_WEIGHT
        #self.h += ang * ANGLE_WEIGHT * 0.8
        self.hash = truncate(self.position.x,PRECISION) +","+truncate(self.position.y,PRECISION)+","+truncate(self.rotation.x,PRECISION)+","+truncate(self.rotation.y,PRECISION)+","+str(self.forward)

    def __lt__(self, other):
        return self.f + self.h < other.f + other.h

    def __eq__(self, other):
        res = False
        if isinstance(other,state):
            res = ( self.position == other.position and self.rotation.get_angle(other.rotation) < 0 )
        else:
            return False

    def getRoute(self):
        p = self
        res = []
        while p !=0:
            if isinstance(p, state) :
                if p.forward == 0 :
                    leftSpeed = ZUMO_WHEELDISTANCE /2 *math.sin(p.rotateArc) / DeltaT * ZUMOVVSREALV * -1
                    rightSpeed = -leftSpeed
                    if(abs(leftSpeed) > 250):
                        print("nonono")
                    leftSpeed = int(leftSpeed)
                    rightSpeed = int(rightSpeed)
                else:
                    leftSpeed = (SPEED * DeltaT - ZUMO_WHEELDISTANCE * math.sin(p.rotateArc)) / DeltaT * p.forward
                    leftSpeed = int(leftSpeed * ZUMOVVSREALV)
                    if (abs(leftSpeed) > 250) :
                        leftSpeed = getSign(leftSpeed) * 250
                        print("nonono")
                    rightSpeed = (SPEED * DeltaT + ZUMO_WHEELDISTANCE * math.sin(p.rotateArc)) /DeltaT * p.forward
                    rightSpeed = int(rightSpeed * ZUMOVVSREALV)
                    if (abs(rightSpeed) > 250) :
                        rightSpeed = getSign(rightSpeed) * 250
                        print("nonono")
                leftSpeed = makeN(leftSpeed)
                rightSpeed = makeN(rightSpeed)
                res.insert(0, [p.position,p.rotation,p.rotateArc,leftSpeed,rightSpeed])
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

        if True :
            print(current_state.f + current_state.h )
        if current_state.position == goal_pos and current_state.rotation.get_angle(goal_rot) < ALMOST_ZERO :
            return current_state.getRoute()

        if current_state.position == goal_pos :
            arcDegree = current_state.rotation.get_angle(goal_rot)
            if not (current_state.rotation.rotate(arcDegree).get_angle(goal_rot) < ALMOST_ZERO) :
                arcDegree = -arcDegree
            if (abs(arcDegree) > MAX_ROTATE):
                temp = abs(arcDegree)
                newpos = current_state.position
                newrot = current_state.rotation.rotate(getSign(arcDegree) * MAX_ROTATE).normalization()
                childstate = state(newpos, newrot, current_state, goal_pos, goal_rot, 0)
                childstate.rotateArc = getSign(arcDegree) * MAX_ROTATE
                temp = abs(temp) - MAX_ROTATE
                while temp > 0:
                    newpos = childstate.position
                    newrot = childstate.rotation.rotate(getSign(arcDegree) * MAX_ROTATE).normalization()
                    childstate = state(newpos, newrot, childstate, goal_pos, goal_rot, 0)
                    childstate.rotateArc = getSign(arcDegree) * MAX_ROTATE
                    temp -= MAX_ROTATE
                newrot = childstate.rotation.rotate(getSign(arcDegree) * (temp + MAX_ROTATE)).normalization()
                newpos = childstate.position + newrot * ONE
                childstate = state(newpos, newrot, childstate, goal_pos, goal_rot, 0)
                childstate.rotateArc = getSign(arcDegree) * (temp + MAX_ROTATE)
            return childstate.getRoute()

        possbilePoint = 0
        for i in range(-60 , 61 , ROT_ANGLE) :
            arcDegree = i * PI / 180
            radius = math.sqrt(ZUMO_WIDTH * ZUMO_WIDTH / 4 + (ONE + ZUMO_LENGTH / 2) * (ONE + ZUMO_LENGTH / 2))
            point1 = current_state.position + current_state.rotation.rotate(arcDegree + PI * ROT_ANGLE / 360).norm_mul(radius)
            point2 = current_state.position + current_state.rotation.rotate(arcDegree - PI * ROT_ANGLE / 360).norm_mul(radius)

            okchild = True

            for oo in obstacle_list :
                if lineWithPolygon(point1,point2,oo):
                    okchild = False
                    break
                if compl_inside_convex(point1,oo) or compl_inside_convex(point2,oo) :
                    okchild = False

            if okchild :
                newpos = 0
                newrot = 0
                childstate = 0
                if (abs(arcDegree) > MAX_ROTATE):
                    temp = abs(arcDegree)
                    newpos = current_state.position
                    newrot = current_state.rotation.rotate(getSign(arcDegree)*MAX_ROTATE).normalization()
                    childstate = state(newpos, newrot, current_state, goal_pos, goal_rot, 0)
                    childstate.rotateArc = getSign(arcDegree)*MAX_ROTATE
                    temp = abs(temp) - MAX_ROTATE
                    while temp > 0 :
                        newpos = childstate.position
                        newrot = childstate.rotation.rotate(getSign(arcDegree) * MAX_ROTATE).normalization()
                        childstate = state(newpos, newrot, childstate, goal_pos, goal_rot, 0)
                        childstate.rotateArc = getSign(arcDegree)*MAX_ROTATE
                        temp -= MAX_ROTATE
                    newrot = childstate.rotation.rotate(getSign(arcDegree) * (temp + MAX_ROTATE)).normalization()
                    newpos = childstate.position + newrot * ONE
                    childstate = state(newpos, newrot, childstate, goal_pos, goal_rot, 0)
                    childstate.rotateArc = getSign(arcDegree)*(temp + MAX_ROTATE)
                else:
                    newrot = current_state.rotation.rotate(arcDegree).normalization()
                    newpos = current_state.position + newrot * ONE
                    childstate = state(newpos, newrot, current_state, goal_pos, goal_rot)
                    childstate.rotateArc = arcDegree
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












