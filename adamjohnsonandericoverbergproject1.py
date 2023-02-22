"""
Class: CS 330
Authors: Adam Johnson & Erik Overberg
Program: Assignment 1
"""


import math
import numpy as np

CONTINUE = 1
FLEE = 2
SEEK = 3
ARRIVE = 4


"""calculate length of 2D vector"""
def vector_length(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

"""normalize vector"""
def normalize(vector):
    length = vector_length(vector)
    if length == 0:
        return vector
    result = np.array([vector[0] / length, vector[1] / length])
    return result

"""Calculate scalar dot product of two 2D vectors"""
def vector_dot(A, B)
    return np.sum(A * B)

"""Find point on line closest to query point in 2D."""
"""Q is the query point, A and B are distinct points on the line, as vectors"""
def closest_point_line(Q, A, B)
    T = vector_dot((Q - A), (B - A)) / vector_dot((B - A), (B - A))
    return(A + (T * (B - A)))

"""FInd point on segment closest to query point in 2D."""
"""Q is the query point, A and B are endpoints of the segment, as vectors."""
def closest_point_segment(Q, A, B)
    T = vector_dot((Q - A), (B - A)) / vector_dot((B - A), (B - A))
    if T <= 0:
        return A
    elif T >= 1:
        return B
    else:
        return A + (T * (B - A))
        

"""class for steering output of characters"""
class steering_output(object):
    def __init__(self):
        self.linear = np.array([0.0, 0.0])
        self.angular = 0.0

"""class to create character instances"""
class character:
    """Initialize general movement"""
    def __init__(self, id: str = None, steer: int = 0, position: np.array = ([0, 0]), velocity: np.array = ([0, 0]),
                 linear: np.array = ([0, 0]), orientation: float = 0, rotation: float = 0, angular: float = 0,
                 max_velocity: float = 0,
                 max_linear: float = 0, target: int = 0, target_radius: int = 0, arrive_radius: float = 0,
                 arrive_slow: float = 0,
                 arrive_time: float = 1, max_acceleration: float = 0):
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
        self.target_radius = target_radius
        self.arrive_radius = arrive_radius
        self.arrive_slow = arrive_slow
        self.arrive_time = arrive_time
        self.max_acceleration = max_acceleration


"""scenario for different character's behavior"""


"""Define steering behaviors"""


def steering_continue(mover):
    """Continue moving without changing direction"""
    result = steering_output()
    result.linear = mover.linear
    result.angular = mover.angular
    return result


"""note: mover is the character"""
def steering_seek(mover, target): 
    """Seek; move directly towards target as fast as possible."""
    result = steering_output()
    """Get the direction to the target."""
    result.linear[0] = target.position[0] - mover.position[0]  """gets direction to move based on target's position"""
    result.linear[1] = target.position[1] - mover.position[1]  """gets direction to move based on target's position"""
    """Give full acceleration along this direction."""
    result.linear = normalize(result.linear)  """normalizes the vector"""
    result.linear = result.linear * mover.max_linear
    result.angular = 0
    return result


#
def steering_flee(mover, target):  # steering id = 3
    """Flee;  move directly away from target as fast as possible."""
    result = steering_output()
    """Get the direction to the target."""
    result.linear[0] = mover.position[0] - target.position[0]  """gets direction to move based on target's position"""
    result.linear[1] = mover.position[1] - target.position[1]  """gets direction to move based on target's position"""
    """Give full acceleration along this direction."""
    result.linear = normalize(result.linear) """normalizes the vector"""
    result.linear = result.linear * mover.max_linear
    result.angular = 0
    return result


def steering_arrive(mover, target):  
    """Arrive; move directly towards target, slowing down when near."""
    result = steering_output()
    """Get the direction to the target."""
    direction = np.array([float, float])
    direction[0] = target.position[0] - mover.position[0]
    direction[1] = target.position[1] - mover.position[1]
    distance = vector_length(direction)
    """Check if we are, return no steering"""
    if distance < mover.target_radius:
        mover.velocity = 0
    """If we are outside the slowRadius, then move at max speed."""
    if distance < mover.arrive_radius:  """"slow down when in range"""
        arrive_speed = 0
    elif distance > mover.arrive_slow:  """set speed to max otherwise"""
        arrive_speed = mover.max_velocity
    else:
        arrive_speed = mover.max_velocity * distance / mover.arrive_slow
    """The target velocity combines speed and direction"""
    arrive_velocity = normalize(direction) * arrive_speed
    result.linear[0] = arrive_velocity[0] - mover.velocity[0]
    result.linear[1] = arrive_velocity[1] - mover.velocity[1]
    result.linear[0] = result.linear[0] / mover.arrive_time
    result.linear[1] = result.linear[1] / mover.arrive_time
    """resets the vector"""
    if vector_length(result.linear) > mover.max_linear:  
        result.linear = normalize(result.linear)
        result.linear = result.linear * mover.max_linear
    result.angular = 0
    return result


def dynamic_update(mover, steering, time):
    result = steering_output()
    """Update Position and orientation"""
    mover.position[0] = mover.position[0] + mover.velocity[0] * time
    mover.position[1] = mover.position[1] + mover.velocity[1] * time
    mover.orientation = mover.orientation + mover.rotation * time

    """Update Velocity and linear displacement"""
    acceleration = steering.linear  """get the desired acceleration from the steering behavior"""
    mover.velocity[0] = mover.velocity[0] + acceleration[0] * time  """update the velocity by adding the acceleration"""
    mover.velocity[1] = mover.velocity[1] + acceleration[1] * time  """update the velocity by adding the acceleration"""
    if vector_length(mover.velocity) > mover.max_velocity:  """clip the velocity to the max linear speed"""
        mover.velocity = normalize(mover.velocity)
        mover.velocity = mover.velocity * mover.max_velocity
    mover.linear = steering.linear
    mover.angular = steering.angular
    return mover


def main():
    character1 = character(id="2601", steer=CONTINUE)
    character2 = character(id="2502", steer=FLEE, position=[-30, -50], velocity=[2, 7], orientation=math.pi / 4,
                           rotation=8, max_velocity=8,
                           max_linear=2, target=1, max_acceleration=1.5)
    character3 = character(id="2503", steer=SEEK, position=[-50, 40], velocity=[0, 8], orientation=3 * math.pi / 2,
                           rotation=8,
                           max_linear=2, max_velocity=8, target=1, max_acceleration=2)
    character4 = character(id="2504", steer=ARRIVE, position=[50, 75], velocity=[-9, 4], orientation=math.pi,
                           rotation=8,
                           max_linear=2, max_velocity=10, max_acceleration=2, target=1, arrive_radius=4, arrive_slow=32)

    characters = [character1, character2, character3, character4]
    time = 0
    delta_time = 0.50
    time_stop = 50
    with open("trajectoryfile.txt", "w") as f:  """creates a file and writes in all trajectory data"""
        while time <= time_stop:
            for i in range(len(characters)):
                if characters[i].steer == CONTINUE:
                    steering = steering_continue(characters[i])
                elif characters[i].steer == SEEK:
                    steering = steering_seek(characters[i], character1)
                    characters[i].linear = steering.linear
                elif characters[i].steer == FLEE:
                    steering = steering_flee(characters[i], character1)
                    characters[i].linear = steering.linear
                elif characters[i].steer == ARRIVE:
                    steering = steering_arrive(characters[i], character1)
                    characters[i].linear = steering.linear
                characters[i] = dynamic_update(characters[i], steering, delta_time)
                f.write(str(time))
                f.write(",")
                f.write(str(characters[i].id))
                f.write(",")
                f.write(str(characters[i].position[0]))
                f.write(",")
                f.write(str(characters[i].position[1]))
                f.write(",")
                f.write(str(characters[i].velocity[0]))
                f.write(",")
                f.write(str(characters[i].velocity[1]))
                f.write(",")
                f.write(str(characters[i].linear[0]))
                f.write(",")
                f.write(str(characters[i].linear[1]))
                f.write(",")
                f.write(str(characters[i].orientation))
                f.write(",")
                f.write(str(characters[i].steer))
                f.write(",")
                f.write("FALSE")
                f.write("\n")
            time = time + delta_time


if __name__ == main():
    main()
