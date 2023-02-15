# Class: CS 330
# Authors: Adam Johnson & Erik Overberg
# Program: Assignment 1
# initialize steering behavior

#TODO::
# Implement plotting (given by prof)
# Implement the loop to update the values
# Continue movement function (take in movements and return the same value)
import math
import numpy as np


# calculate length of 2D vector
def vector_Length(v):
    return (math.sqrt(v[0] ** 2 + v[1] ** 2))


class Character:
    CONTINUE = 1
    FLEE = 6
    SEEK = 7
    ARRIVE = 8

    # Initialize general movement
    def __init__(self, id: str = None, steer: int = 0, position: np.array = ([0, 0]), velocity: np.array = ([0, 0]),
                 linear: np.array = ([0, 0]), orientation: float = 0, rotation: float = 0, angular: float = 0,
                 max_velocity: float = 0,
                 max_linear: float = 0, target: int = 0, arrive_radius: float = 0, arrive_slow: float = 0,
                 arrive_time: float = 0):
        self.id = id
        self.steer = steer
        self.position = position
        self.velocity = velocity
        self.linear = linear
        self.orientation = orientation
        self.rotation = rotation
        self.angular = angular
        self.max_velocity = max_velocity
        self.max_linear = max_linear
        self.target = target
        self.arrive_radius = arrive_radius
        self.arrive_slow = arrive_slow
        self.arrive_time = arrive_time


# scenario for different character's behavior


# Define steering behaviors


def GetSteeringContinue(self):
    # Continue moving without changing direction
    result = {"linear": self.linear, "angular": self.angular}
    return result


def GetSteeringSeek(self, target):
    # Seek; move directly towards target as fast as possible.
    result = Character(self.position, self.linear, self.angular)
    self.linear = target.position - self.position # gets direction to move based on target's position
    self.linear = np.linalg.norm(self.linear) # normalizes the vector
    self.linear *= self.max_linear
    self.angular = 0
    return result


def GetSteeringFlee(self, target):
    # Flee;  move directly away from target as fast as possible.
    result = Character()
    self.linear = self.position - target.position # calculates direction in which to flee
    self.linear = np.linalg.norm(self.linear) # normalizes the vector
    self.linear *= self.max_linear
    self.angular = 0
    return result


def GetSteeringArrive(self, target):
    # Arrive; move directly towards target, slowing down when near.
    result = Character()
    direction = target.position - self.position
    distance = np.linalg.norm(direction)
    if distance < self.arrive_radius: # slow down when in range
        arrive_speed = 0
    elif distance > self.arrive_radius: # set speed to max otherwise
        arrive_speed = self.max_velocity
    else:
        arrive_speed = self.max_velocity * distance / self.arrive_radius
    arrive_velocity = np.linalg.norm(direction) * arrive_speed
    result.linear = arrive_velocity - self.velocity
    result.linear = result.linear / self.arrive_time
    if np.linalg.norm(result.linear) > self.max_linear: # resets the vector
        result.linear = np.linalg.norm(result.linear)
        result.linear = result.linear * self.max_linear
    return result


def DynamicUpdate(self, steering, max_speed, time): # This is the movement update function on the rubric
    # Update Position and orienatation
    self.position += self.velocity * time
    self.orientation += self.rotation * time
    # Update Velocity and rotation
    self.velocity += self.linear * time
    self.rotation += steering.linear * time
    self.rotation += steering.angular * time
    # Check for speed and clip
    speed = np.linalg.norm(self.velocity)
    if speed > max_speed:
        self.velocity = self.velocity / speed * max_speed


def main():
    character1 = Character(id=2601, steer=1)
    character2 = Character(id=2502, steer=2, position=[-30, -50], velocity=[2, 7], orientation=math.pi / 2, rotation=8,
                           max_linear=2, target=1)
    character3 = Character(id=2503, steer=3, position=[-50, 40], velocity=[0, 8], orientation=math.pi / 2, rotation=8,
                           max_linear=2, target=1)
    character4 = Character(id=2504, steer=4, position=[50, 75], velocity=[-9, 4], orientation=math.pi / 2, rotation=8,
                           max_linear=2, target=1)

    characters = [character1, character2, character3, character4]

    delta_time = 0.50
    time_stop = 50
    steps_total = time_stop / delta_time

    with open("trajectoryfile", "w") as f: # creates a file and writes in all trajectory data
        for i, char in enumerate(characters):
            char_out = "0,{},{},{},{},{},{},{},{},{},{}\n".format(char.id, )
