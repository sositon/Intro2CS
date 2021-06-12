import math


class Asteroid:
    MIN_SIZE = 1
    MAX_SIZE = 3
    TEN = 10
    FIVE = 5
    """The class Asteroid represents a asteroid object and getting the location, the speed and the size of the asteroid.
    The constructor contain: the location, speed, radius and the size of the asteroid"""

    def __init__(self, location_x, location_y, speed_x, speed_y, size):
        self.__location_x = location_x
        self.__location_y = location_y
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__size = size
        self.__radius = size * self.TEN - self.FIVE

    def get_location_x(self):
        """This method returns - location x."""
        return self.__location_x

    def get_location_y(self):
        """This method returns - location y."""
        return self.__location_y

    def get_speed_x(self):
        """This method returns - speed x."""
        return self.__speed_x

    def get_speed_y(self):
        """This method returns - speed y."""
        return self.__speed_y

    def get_size(self):
        """This method returns - size of the asteroid."""
        return self.__size

    def get_radius(self):
        """This method returns - radius of the asteroid."""
        return self.__radius

    def set_location(self, x, y):
        """This method gets the new location for the asteroid and sets it."""
        self.__location_x = x
        self.__location_y = y

    def set_speed(self, x, y):
        """This method gets the speed for the asteroid and sets it."""
        self.__speed_x = x
        self.__speed_y = y

    def set_size(self, new_asteroid_size):
        """This method gets the new size of the asteroid and sets it."""
        self.__size = new_asteroid_size

    def has_intersection(self, obj):
        """
        :param obj: An object from other class
        :return: True if an asteroid intersect the object and False otherwise
        """
        distance = math.sqrt((obj.get_location_x() - self.get_location_x())
                             ** 2 + (obj.get_location_y() -
                             self.get_location_y()) ** 2)
        if distance <= self.get_radius() + obj.get_radius():
            return True
        return False
