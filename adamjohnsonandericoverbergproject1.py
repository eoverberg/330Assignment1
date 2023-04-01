"""
Class: CS 330
Authors: Adam Johnson & Erik Overberg
Program: Assignment 2
"""

import math
import numpy as np

ASSIGNMENT = 2

"""initialize steering behavior constraints"""
CONTINUE = 1
FLEE = 6
SEEK = 7
ARRIVE = 8
FOLLOWPATH = 11

"""calculate length of 2D vector"""


def length(vector):
    length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    return length


"""normalize vector (keep direction but make the length = 1"""


def normalize(vector):
    vector_length = length(vector)
    if vector_length == 0:
        return vector
    result = np.array([vector[0] / vector_length, vector[1] / vector_length])
    return result


"""Calculate scalar dot product of two 2D vectors"""


def vector_dot(A, B):
    return np.sum(A * B)


"""calculate Euclidean distance between two points in 2D"""


def distance_point_point(point_a, point_b):
    return math.sqrt(sum([(point_a[i] - point_b[i]) ** 2 for i in range(2)]))  #


#
# """Find point on line closest to query point in 2D."""
# """Q is the query point, A and B are distinct points on the line, as vectors"""
#
#
# def closest_point_line(Q, A, B):
#     T = vector_dot((Q - A), (B - A)) / vector_dot((B - A), (B - A))
#     return (A + (T * (B - A)))
#
#
# """FInd point on segment closest to query point in 2D."""
# """Q is the query point, A and B are endpoints of the segment, as vectors."""
#
#
# def closest_point_segment(Q, A, B):
#     T = vector_dot((Q - A), (B - A)) / vector_dot((B - A), (B - A))
#     if T <= 0:
#         return A
#     elif T >= 1:
#         return B
#     else:
#         return A + (T * (B - A))
#
#
# """Assemble a complete path data structure from its coordinates"""
#
#
# def path_assemble(path_id, path_x, path_y):
#     path_segments = len(path_x) - 1
#     path_distance = np.zeros(path_segments + 1)
#     for i in range(1, path_segments + 1):
#         path_distance[i] = path_distance[i - 1] + distance_point_point([path_x[i - 1], path_y[i - 1]],
#                                                                        [path_x[i], path_y[i]])
#     path_param = np.zeros(path_segments + 1)
#     for i in range(1, path_segments + 1):
#         path_param[i] = path_distance[i] / max(path_distance)
#     return path_id, path_x, path_y, path_distance, path_param, path_segments
#
#
# """Caclulate position on path"""
#
#
# def path_position(path, param):
#     if param <= path.param[0]:
#         return np.array([path.x[0], path.y[0]])
#     i = max(np.where(param > path.param)[0])
#     """Find segment S on path H with endpoints A and B"""
#     A = np.array([path.x[i], path.y[i]])
#     B = np.array([path.x[i + 1], path.y[i + 1]])
#     T = (param - path.param[i]) / (path.param[i + 1] - path.param[i])
#     P = A + T * (B - A)
#     return P
#
#
# def path_param(path, position):
#     """Find point on path closest to given position"""
#     closest_distance = np.inf
#     for i in range(1, path.segments):
#         A = np.array([path.x[i - 1], path.y[i - 1]])
#         B = np.array([path.x[i], path.y[i]])
#         check_point = closest_point_segment(position, A, B)
#         check_distance = distance_point_point(position, check_point)
#         if check_distance < closest_distance:
#             closest_point = check_point
#             closest_distance = check_distance
#             closest_segment = i
#
#     return closest_segment
#

# Path functions
def closest_point_segment(Q, A, B):
    T = np.dot((Q - A), (B - A)) / np.dot((B - A), (B - A))
    if T <= 0:
        return A
    elif T >= 1:
        return B
    else:
        return A + T * (B - A)


# Assemble a complete path data structure from its coordinates.
def assemble_path(path_id, path_x, path_y):
    path_segments = len(path_x) - 1
    path_distance = [0] * (path_segments + 1)
    for i in range(1, path_segments + 1):
        path_distance[i] = path_distance[i - 1] + distance_point_point([path_x[i - 1], path_y[i - 1]],
                                                                       [path_x[i], path_y[i]])
    path_param = [0] * (path_segments + 1)
    for i in range(1, path_segments + 1):
        path_param[i] = path_distance[i] / max(path_distance)
    return {"id": path_id, "x": path_x, "y": path_y, "distance": path_distance, "param": path_param,
            "segments": path_segments}


# Calculate the position on a path corresponding to a given path parameter.
def get_path_position(path, param):
    i = max([j for j in range(len(path["param"])) if param > path["param"][j]])
    A = [path["x"][i], path["y"][i]]
    B = [path["x"][i + 1], path["y"][i + 1]]
    T = (param - path["param"][i]) / (path["param"][i + 1] - path["param"][i])
    P = [A[k] + (T * (B[k] - A[k])) for k in range(2)]
    return P


# Find the path parameter of the point on the path closest to a given position.
def get_path_param(path, position):
    # Find point on path closest to given position.

    closest_distance = math.inf
    for i in range(1, path.segments):
        A = [path["x"][i], path["y"][i]]
        B = [path["x"][i + 1], path["y"][i + 1]]
        check_point = closest_point_segment(position, A, B)
        check_distance = distance_point_point(position, check_point)
        if check_distance < closest_distance:
            closest_point = check_point
            closest_distance = check_distance
            closest_segment = i

    # Calculate path parameter of closest point; see. p. 70.136.

    A = [path["x"][closest_segment], path["y"][closest_segment]]
    A_param = path["param"][closest_segment]
    B = [path["x"][closest_segment + 1], path["y"][closest_segment + 1]]
    B_param = path["param"][closest_segment + 1]
    C = closest_point
    T = length([C[k] - A[k] for k in range(2)]) / length([B[k] - A[k] for k in range(2)])
    C_param = A_param + (T * (B_param - A_param))

    return C_param


"""class for steering output of characters"""


class steering_output(object):
    def __init__(self):
        self.linear = np.array([0.0, 0.0])
        self.angular = 0.0


"""class to create character instances"""


class Character:
    """Initialize general movement"""

    def __init__(self, id: str = None, steer: int = 0, position: np.array = np.array([0, 0]),
                 velocity: np.array = np.array([0, 0]),
                 linear: np.array = np.array([0, 0]), orientation: float = 0, rotation: float = 0, angular: float = 0,
                 max_velocity: float = 0,
                 max_linear: float = 0, target: int = 0, target_radius: int = 0, arrive_radius: float = 0,
                 arrive_slow: float = 0,
                 arrive_time: float = 1, max_acceleration: float = 0, path_to_follow: int = 0, path_offset: float = 0):
        self.colCollided = None
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
        self.path_to_follow = path_to_follow
        self.path_offset = path_offset


"""class for path instances"""


class Path:
    """initialize array for path"""

    def __init___(self, id: str = None, x: np.array = np.array([0, 0]), y: np.array = np.array([0, 0]),
                  params: np.array = np.array([0, 0]),
                  distance: np.array = np.array([0, 0]), segments: int = 0):
        self.id = id
        """Array of x coordinates"""
        self.x = x
        """Array of y coordinates"""
        self.y = y
        """Array of path parameters at each vertex"""
        self.params = params
        """Array of path distance at each vertex"""
        self.distance = distance
        """Number of segments in the path"""
        self.segments = segments


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
    """gets direction to move based on target's position"""
    result.linear[0] = target.position[0] - mover.position[0]
    result.linear[1] = target.position[1] - mover.position[1]
    """Give full acceleration along this direction."""
    """normalizes the vector"""
    result.linear = normalize(result.linear)
    result.linear = result.linear * mover.max_linear
    result.angular = 0
    return result


def steering_flee(mover, target):
    """Flee;  move directly away from target as fast as possible."""
    result = steering_output()
    """Get the direction to the target."""
    result.linear[0] = mover.position[0] - target.position[0]
    result.linear[1] = mover.position[1] - target.position[1]
    """Give full acceleration along this direction."""
    """normalizes the vector"""
    result.linear = normalize(result.linear)
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
    distance = length(direction)
    """Check if we are, return no steering"""
    if distance < mover.target_radius:
        mover.velocity = 0
    """If we are outside the slowRadius, then move at max speed."""
    """slow down when in range"""
    if distance < mover.arrive_radius:
        arrive_speed = 0
    """set speed to max otherwise"""
    if distance > mover.arrive_slow:
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
    if length(result.linear) > mover.max_linear:
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
    """get the desired acceleration from the steering behavior"""
    acceleration = steering.linear
    mover.velocity[0] = mover.velocity[0] + acceleration[0] * time
    mover.velocity[1] = mover.velocity[1] + acceleration[1] * time
    """clip the velocity to the max linear speed"""
    if length(mover.velocity) > mover.max_velocity:
        mover.velocity = normalize(mover.velocity)
        mover.velocity = mover.velocity * mover.max_velocity
    mover.linear = steering.linear
    mover.angular = steering.angular
    return mover


def steering_follow_path(mover, path):
    current_param = get_path_param(path, mover.position)
    target_param = min(1, current_param + mover.path_offset)
    target_position = path.get_position(path, target_param)
    target = {"position": target_position}
    return steering_seek(mover, target)


def main():
    time = 0.0
    # if ASSIGNMENT == 1:
    #     delta_time = 0.50
    #     time_stop = 50
    #     character1 = Character(id="2601", steer=CONTINUE)
    #     character2 = Character(id="2502", steer=FLEE, position=[-30, -50], velocity=[2, 7], orientation=math.pi / 4,
    #                            rotation=8, max_velocity=8, max_linear=2, target=1, max_acceleration=1.5)
    #     character3 = Character(id="2503", steer=SEEK, position=[-50, 40], velocity=[0, 8], orientation=3 * math.pi / 2,
    #                            rotation=8, max_linear=2, max_velocity=8, target=1, max_acceleration=2)
    #     character4 = Character(id="2504", steer=ARRIVE, position=[50, 75], velocity=[-9, 4], orientation=math.pi,
    #                            rotation=8, max_linear=2, max_velocity=10, max_acceleration=2, target=1, arrive_radius=4,
    #                            arrive_slow=32)
    #
    #     characters = [character1, character2, character3, character4]

    """instance of character object for assignment 2"""
    # if ASSIGNMENT == 2:
    delta_time = 0.50
    time_stop = 125
    """new character"""
    character5 = Character(id="2701", steer=FOLLOWPATH, position=[20, 95], velocity=[0, 0], orientation=0,
                           max_velocity=4, max_linear=2, path_to_follow=1, path_offset=0.04)
    characters = [character5]

    """creates a file and writes in all trajectory data"""
    filename = 'CS330 Assignment ' + str(ASSIGNMENT) + ' output.txt'
    """creates file if one does not exist"""
    f = open(filename, 'w')
    """print time 0 initial conditions to console"""
    for character in characters:
        print(time, character.id, character.position[0], character.position[1], character.velocity[0],
              character.velocity[1], character.linear[0], character.linear[1], character.orientation,
              character.steer, character.colCollided, sep=", ", end="\n", file=f)
    f.close()

    """main while loop"""
    while time < time_stop:
        time = time + delta_time

        """loop through all characters and execute relevant steering behavior"""
        for character in characters:
            if character.steer == CONTINUE:
                steering = steering_continue(character)
            elif character.steer == SEEK:
                steering = steering_seek(character, character.target.position)
            elif character.steer == FLEE:
                steering = steering_flee(character, character.target.position)
            elif character.steer == ARRIVE:
                steering = steering_arrive(character, character.target.position)
                characters.linear = steering.linear
            elif character.steer == FOLLOWPATH:
                if character.path_to_follow == 1:
                    path = Path()
                    x = (0, -20, 20, -40, 40, -60, 60, 0)
                    y = (90, 65, 40, 15, -10, -35, -60, -85)
                    assemble_path(1, x, y)
                steering = steering_follow_path(character, path)

            """calculate updates"""
            character = dynamic_update(character, steering, delta_time)

        """cycle through characters and print updated conditions"""
        """append to output file"""
        f = open(filename, 'a')
        for character in characters:
            print(time, character.id, character.position[0], character.position[1], character.velocity[0],
                  character.velocity[1], character.linear[0], character.linear[1], character.orientation,
                  character.steer, character.colCollided, sep=", ", end="\n", file=f)
        f.close()


if __name__ == main():
    main()
