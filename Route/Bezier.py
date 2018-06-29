#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Route import Astar

from Route.Vector2 import *

def binomial(i, n):
    """Binomial coefficient"""
    return math.factorial(n) / float(
        math.factorial(i) * math.factorial(n - i))


def bernstein(t, i, n):
    """Bernstein polynom"""
    return binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))


def bezier(t, points):
    """Calculate coordinate of a point in the bezier curve"""
    n = len(points) - 1
    x = y = 0
    for i, pos in enumerate(points):
        bern = bernstein(t, i, n)
        x += pos.x * bern
        y += pos.y * bern
    return Vector2(x, y)


def bezier_curve_range(n, points):
    """Range of points in a curve bezier"""
    for i in range(n):
        t = i / float(n - 1)
        yield bezier(t, points)


def findRoute(start_pos, start_rot, goal_pos, goal_rot):
    interP = intersection(start_pos, start_rot, goal_pos, goal_rot)
    round = (goal_pos - start_pos).x * (goal_pos - start_pos).x + (goal_pos - start_pos).y * (
                goal_pos - start_pos).y
    round = int(round / 4 * PI) + 1
    ctrlPoints = [start_pos, (start_pos + interP) * 0.5, (interP + goal_pos) * 0.5, goal_pos]
    routePoint = []
    for point in bezier_curve_range(round, ctrlPoints):
        routePoint.append(point)

    state = Astar.state(start_pos, start_rot, 0, goal_pos, goal_pos)
    childRot = routePoint[1] - routePoint[0]
    state.rotateArc = leftOrRight(routePoint[0],start_rot,routePoint[1]) * start_rot.get_angle(childRot)
    for i in range(1,len(routePoint)-1):
        state = Astar.state(routePoint[i], childRot, state, goal_pos, goal_rot)
        childRot = routePoint[i+1] - routePoint[i]
        state.rotateArc = leftOrRight(routePoint[i],state.rotation,routePoint[i+1]) * state.rotation.get_angle(childRot)

    state = Astar.state(goal_pos, goal_rot, state, goal_pos, goal_rot)
    state.rotateArc = 0
    return state.getRoute()


