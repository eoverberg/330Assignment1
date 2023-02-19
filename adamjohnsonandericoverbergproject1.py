# Class: CS 330
# Authors: Adam Johnson & Erik Overberg
# Program: Assignment 1
# initialize steering behavior

# TODO::
# Implement the loop to update the values
# Continue movement function (take in movements and return the same value)
import math


CONTINUE = 1
FLEE = 6
SEEK = 7
ARRIVE = 8
# calculate length of 2D vector
def vector_length(vector):
    return (math.sqrt(vector[0] ** 2 + vector[1] ** 2))
#normalize vector
def normalize(vector)
    vector_length = length(vector)
    if vector_length == 0:
        return vector
    result = np.array([vector[0]/vector_length, vector[1]/vector_length)
    return result
        


class character:
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
        self.target_radius = target_radius
        self.arrive_radius = arrive_radius
        self.arrive_slow = arrive_slow
        self.arrive_time = arrive_time
        
class steering_output:
    def __init__(self, linear: List[float)= [0,0], angular = 0):
        self.linear = linear
        self.angular = angular


# scenario for different character's behavior



# Define steering behaviors


def steering_continue(character):
    # Continue moving without changing direction
    result = steering_output()
    result.linear = character.linear
    result.angular = character.angular
    return result

#note: mover is the character
def steering_seek(mover, target):  # steering ds = 2
    # Seek; move directly towards target as fast as possible.
    result = steering_output()
    # Get the direction to the target.
    result.linear = target.position - mover.position 
    
    # Give full acceleration along this direction.
    result.linear = normalize(result.linear)  # normalizes the vector
    result.linear = result.linear * mover.max_linear
    result.angular = 0
    return result

#
def steering_flee(mover, target):  # steering id = 3
    # Flee;  move directly away from target as fast as possible.
    result = steering_output()
    # Get the direction to the target.
    result.linear = mover.position - target.position  # gets direction to move based on target's position
    
    # Give full acceleration along this direction.
    result.linear = normalize(result.linear)  # normalizes the vector
    result.linear = result.linear * mover.max_linear
    result.angular = 0
    return result


def steering_arrive(mover, target):  # steering id = 4 
    # Arrive; move directly towards target, slowing down when near.
    result = steering_output()
    # Get the direction to the target.                             
    direction = target.position - mover.position 
    distance = normalize(direction)
    # check if we are, return no steering
    if distance < target_radius
        return null
    # If we are outside the slowRadius, then move at max speed.
    if distance < mover.arrive_radius:  # slow down when in range
        arrive_speed = 0
    elif distance > mover.arrive_slow:  # set speed to max otherwise
        arrive_speed = mover.max_velocity
    else:
        arrive_speed = mover.max_velocity * distance / mover.arrive_slow
    #The target velocity combines speed and direction
    arrive_velocity = np.linalg.norm(direction) * arrive_speed
    result.linear = arrive_velocity - self.velocity
    result.linear = result.linear / self.arrive_time
    if np.linalg.norm(result.linear) > self.max_linear:  # resets the vector
        result.linear = np.linalg.norm(result.linear)
        result.linear = result.linear * self.max_linear
    return result


def dynamic_update(self, steering, time):  # This is the movement update function on the rubric
    # Update Position and orientation
    self.position[0] = self.position[0] + (self.velocity[0] * time)
    self.position[1] = self.position[1] + (self.velocity[1] * time)
    self.orientation = self.orientation + (self.rotation * time)
    # Update Velocity and rotation
    self.velocity[0] = self.velocity[0] + (self.linear[0] * time)
    self.velocity[1] = self.velocity[1] + (self.linear[1] * time)
#    self.rotation = steering.linear * time + self.rotation
    self.rotation = self.rotation + (steering.angular * time)
    return self


def main():
    character1 = character(id="2601", steer=1)
    character2 = character(id="2502", steer=2, position=[-30, -50], velocity=[2, 7], orientation=math.pi / 2, rotation=8,
                           max_linear=2, target=1)
    character3 = character(id="2503", steer=3, position=[-50, 40], velocity=[0, 8], orientation=math.pi / 2, rotation=8,
                           max_linear=2, target=1)
    character4 = character(id="2504", steer=4, position=[50, 75], velocity=[-9, 4], orientation=math.pi / 2, rotation=8,
                           max_linear=2, target=1)

    characters = [character1, character2, character3, character4]
    time = 0
    delta_time = 0.50
    time_stop = 50
    with open("trajectoryfile.txt", "w") as f:  # creates a file and writes in all trajectory data
        while time <= time_stop:
            for i in range(len(characters)):
                if characters[i].steer == CONTINUE:
                    steering = steering_continue(characters[i])
                elif characters[i].steer == SEEK:
                    steering = steering_seek(characters[i], character1)
                elif characters[i].steer == FLEE:
                    steering = steering_flee(characters[i], character1)
                elif characters[i].steer == ARRIVE:
                    steering = steering_arrive(characters[i], character1)
                characters[i] = dynamic_update(characters[i], steering, time)
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
                f.write("\n")
                time = time + delta_time




if __name__ == main():
    main()
