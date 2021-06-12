class Torpedo:
    TORPEDO_RADIUS = 4
    TORPEDO_LIFE_TIME = 200
    """The class Torpedo represents a torpedo object and getting the location, the speed and the heading.
    The constructor contain: location ,speed, heading, radius and the life time"""

    def __init__(self, location_x, location_y, speed_x, speed_y, heading):
        self.__location_x = location_x
        self.__location_y = location_y
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__heading = heading
        self.__radius = self.TORPEDO_RADIUS
        self.__life_time = self.TORPEDO_LIFE_TIME

    def get_location_x(self):
        """This method returns the location x."""
        return self.__location_x

    def get_location_y(self):
        """This method returns the location y."""
        return self.__location_y

    def get_speed_x(self):
        """This method returns the speed x."""
        return self.__speed_x

    def get_speed_y(self):
        """This method returns the speed y."""
        return self.__speed_y

    def get_heading(self):
        """This method returns the heading."""
        return self.__heading

    def get_radius(self):
        """This method returns the radius."""
        return self.__radius

    def get_life_time(self):
        """This method returns the torpedo life time."""
        return self.__life_time

    def set_location(self, new_x_location, new_y_location):
        """This method gets the new location for the torpedo and sets it."""
        self.__location_x = new_x_location
        self.__location_y = new_y_location

    def set_speed(self, new_x_speed, new_y_speed):
        """This method gets the new speed for the torpedo and sets it."""
        self.__speed_x = new_x_speed
        self.__speed_y = new_y_speed

    def set_heading(self, new_heading):
        """This method gets the new heading of the torpedo and sets it."""
        self.__heading = new_heading

    def set_life_time(self, life_time):
        """this method updates life time for the torpedo """
        self.__life_time = life_time
