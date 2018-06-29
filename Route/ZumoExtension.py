from Route.Vector2 import *
from Route import Bezier, Astar


def rotateAction(ArcAngle) :
    time = makeFour(abs(int(ArcAngle / (0.8 *PI) * 1000)))
    left = makeN(getSign(ArcAngle) * -1 * 100)
    right = makeN(getSign(ArcAngle)*100)
    return [left, right, time]

class ZumoExtension:
    def __init__(self):
        self.position = Vector2(0,0)
        self.rotation = Vector2(0,0)
        self.route = list() #[target points ,target rotation]
        self.action = list()
        self.GETSTEP = [False, False, False] #arrive shoes ,


    def gogoSimple(self,transformInfomation):
        #it always go forward first once and rotate once secondly
        self.position = Vector2(transformInfomation[0], transformInfomation[1])
        self.rotation = Vector2(transformInfomation[2], transformInfomation[3])
        shoes_position = Vector2(transformInfomation[4], transformInfomation[5])
        shoes_rotation = Vector2(transformInfomation[6], transformInfomation[7])
        target_position = Vector2(transformInfomation[8], transformInfomation[9])
        target_rotation = Vector2(transformInfomation[10], transformInfomation[11])

        goal1_pos = shoes_position + Vector2(-1*(SHOES_WIDTH /2 + ZUMO_LENGTH /2),0)
        goal1_rot = shoes_rotation

        goal2_pos = target_position + Vector2(0, -1*(SHOES_LENGTH + ZUMO_LENGTH))
        goal2_rot = target_rotation

        self.route.append(self.position)

        inter1 = Vector2(self.position.x, goal1_pos.y)
        self.route.append(inter1)
        distance = (inter1 - self.position).magnitude()
        left = SPEED * 5
        right = SPEED * 5
        time = makeFour(int(distance / SPEED *1000))
        self.action.append(["+100","+100",time])
        self.action.append(rotateAction(-PI/2))

        inter2 = Vector2 (goal2_pos.x - 0.5 * ZUMO_LENGTH, goal1_pos.y)
        self.route.append(inter2)
        distance = (inter2 - inter1 ).magnitude()
        time = makeFour(int(distance / SPEED * 1000))
        self.action.append(["+100","+100",time])

        inter3 = inter2 + Vector2(-0.3 * ZUMO_LENGTH,0)
        self.route.append(inter3)
        distance = (inter3 - inter2).magnitude()
        self.action.append(["-100","-100", makeFour(int (distance / SPEED * 1000 ))])

        self.action.append(rotateAction(-PI/2))

        inter4 = inter3 + Vector2(0, -1*(0.5 * SHOES_LENGTH + 0.8 * SHOES_WIDTH))
        self.route.append(inter4)
        distance = (inter4 - inter3).magnitude()
        self.action.append(["+100","+100",makeFour( int (distance / SPEED * 1000 ))])

        self.action.append(rotateAction(PI/2))

        inter5 = Vector2(goal2_pos.x, inter4.y)
        self.route.append(inter5)
        distance = (inter5 - inter4).magnitude()
        self.action.append(["+100","+100",makeFour(int (distance / SPEED * 1000 ))])

        self.action.append(rotateAction(PI/2))

        self.route.append(goal2_pos)
        distance = (goal2_pos - inter5).magnitude()
        self.action.append(["+100","+100",makeFour( int (distance / SPEED * 1000 ))])

    def printRoute(self,routelist):
        for i in routelist:
            for j in i:
                print(j)
            print("")

    def superGOGO(self,transformInfomation,obstacle_list):
        self.position = Vector2(transformInfomation[0], transformInfomation[1])
        self.rotation = Vector2(transformInfomation[2], transformInfomation[3])
        shoes_position = Vector2(transformInfomation[4], transformInfomation[5])
        shoes_rotation = Vector2(transformInfomation[6], transformInfomation[7])
        goal_position = Vector2(transformInfomation[8], transformInfomation[9])
        goal_rotation = Vector2(transformInfomation[10], transformInfomation[11])

        goal1_pos = 0
        goal1_rot = 0
        goal2_pos = 0
        goal2_rot = 0
        if True : #not self.GETSTEP[0] :
            goal1_pos = shoes_position + Vector2(-1*(SHOES_WIDTH /2 + ZUMO_LENGTH /2),0)
            goal1_rot = shoes_rotation
            r1 = Astar.FindRoute(self.position, self.rotation, goal1_pos, goal1_rot, obstacle_list)
            #if self.position == goal1_pos and self.rotation == goal1_rot :
                #self.GETSTEP[0] == True

        if True : #self.GETSTEP[0] and not self.GETSTEP[1] :
            goal2_pos = goal_position + Vector2(0, -1*(SHOES_LENGTH + ZUMO_LENGTH))
            goal2_rot = goal_rotation
            r2 = Astar.FindRoute(goal1_pos, goal1_rot, goal2_pos, goal2_rot, obstacle_list)
            #if self.position == goal1_pos and self.rotation == goal1_rot :
            #    self.GETSTEP[1] == True
        r1.extend(r2)
        return r1

    def gogoBezier(self,transformInfomation,):
        self.position = Vector2(transformInfomation[0], transformInfomation[1])
        self.rotation = Vector2(transformInfomation[2], transformInfomation[3])
        shoes_position = Vector2(transformInfomation[4], transformInfomation[5])
        shoes_rotation = Vector2(transformInfomation[6], transformInfomation[7])
        target_position = Vector2(transformInfomation[8], transformInfomation[9])
        target_rotation = Vector2(transformInfomation[10], transformInfomation[11])

        goal1_pos = shoes_position + Vector2(-1 * (SHOES_WIDTH / 2 + ZUMO_LENGTH / 2), 0)
        goal1_rot = shoes_rotation

        goal2_pos = target_position + Vector2(0, -1 * (SHOES_LENGTH + ZUMO_LENGTH))
        goal2_rot = target_rotation

        r1 = Bezier.findRoute(self.position, self.rotation, goal1_pos, goal1_rot)
        r2 = Bezier.findRoute(goal1_pos, goal1_rot, goal2_pos, goal2_rot)
        r1.extend(r2)
        return r1


