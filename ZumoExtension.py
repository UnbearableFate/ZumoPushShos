from Vector2 import *
import math
import Astar


class ZumoExtension:
    def __init__(self):
        self.position = Vector2(0,0)
        self.rotation = Vector2(0,0)
        self.route = list() #[target points ,target rotation]
        self.action = list()
        self.GETSTEP = [False, False, False] #arrive shoes ,

    def zumoControl(self):
        if self.action[0] > ALMOST_ZERO :
            return ["forward", self.action[0]]
        elif self.action[1] > ALMOST_ZERO :
            return ["rotate", self.action[1]]
        else:
            self.action.pop(0)
            return ["forward", self.action[0]]


    def gogoSimple(self,transformInfomation):
        #it always go forward first once and rotate once secondly
        self.position = Vector2(transformInfomation[0], transformInfomation[1])
        self.rotation = Vector2(transformInfomation[2], transformInfomation[3])
        shoes_position = Vector2(transformInfomation[4], transformInfomation[5])
        shoes_rotation = Vector2(transformInfomation[6], transformInfomation[7])
        target_position = Vector2(transformInfomation[8], transformInfomation[9])
        target_rotation = Vector2(transformInfomation[10], transformInfomation[11])

        z_s_routeVec= shoes_position - self.position
        s_t_routeVec = target_position - shoes_position
        
        self.route.append([self.position,self.rotation])
        self.route.append([self.position,Vector2(0,1)])
        if abs(z_s_routeVec.x) > ALMOST_ZERO and abs(z_s_routeVec.y) > ALMOST_ZERO :
            inter = Vector2(0,shoes_position.y)
            self.route.append([inter,Vector2(1,0)])

        self.route.append([shoes_position + Vector2(-1*(SHOES_WIDTH/2 +ZUMO_LENGTH/2),0), Vector2(1,0)])

        if abs(s_t_routeVec.x) > ALMOST_ZERO and abs(s_t_routeVec.y) > ALMOST_ZERO :
            inter = Vector2(target_position.x - SHOES_WIDTH /2 - ZUMO_LENGTH/2,shoes_position.y)
            self.route.append([inter,Vector2(0,-1)])
            self.action.append()

            inter = inter + Vector2(0,-1* (ZUMO_LENGTH/2 + SHOES_LENGTH/2))
            self.route.append([inter,Vector2(1,0)])

            inter = Vector2(target_position.x,shoes_position.y - SHOES_LENGTH/2 - ZUMO_LENGTH/2)
            self.route.append([inter,Vector2(0,1)])

        self.route.append([target_position,Vector2(0,1)])
        for i in range(1,len(self.route)) :
            forward = (self.route[i][0] - self.route[i-1][0]).magnitude()
            rotate = self.route[i][1].get_angle(self.route[i-1][1])
            self.action.append([forward,rotate])

    def gogoPro(self,transformInfomation,obstacle_list):
        self.position.x = transformInfomation[0]
        self.position.y = transformInfomation[1]
        self.rotation = Vector2(transformInfomation[2], transformInfomation[3])
        shoes_position = Vector2(transformInfomation[4], transformInfomation[5])
        shoes_rotation = Vector2(transformInfomation[6], transformInfomation[7])

        rout = Astar.FindRoute(self.position,self.rotation,shoes_position,shoes_rotation,obstacle_list)
        return rout

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
            r1 = Astar.FindRoute(self.position,self.rotation,goal1_pos,goal1_rot,obstacle_list)
            #if self.position == goal1_pos and self.rotation == goal1_rot :
                #self.GETSTEP[0] == True

        if True : #self.GETSTEP[0] and not self.GETSTEP[1] :
            goal2_pos = goal_position + Vector2(0, -1*(SHOES_LENGTH + ZUMO_LENGTH))
            goal2_rot = goal_rotation
            r2 = Astar.FindRoute(goal1_pos,goal1_rot, goal2_pos,goal2_rot,obstacle_list)
            #if self.position == goal1_pos and self.rotation == goal1_rot :
            #    self.GETSTEP[1] == True
        r1.extend(r2)
        return r1