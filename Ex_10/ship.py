class Ship:
    SHIP_RADIUS = 1

    """The class Ship represents a ship object, and getting the location of the ship.
    The constructor contain: location, speed, prow_direction and the radius of the ship"""

    def __init__(self, location_x, location_y, speed_x, speed_y, prow_direction):
        self.__location_x = location_x
        self.__location_y = location_y
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__prow_direction = prow_direction
        self.__radius = self.SHIP_RADIUS

    def get_location_x(self):
        """This method returns- location x."""
        return self.__location_x

    def get_location_y(self):
        """This method returns- location y."""
        return self.__location_y

    def get_speed_x(self):
        """This method returns- speed x."""
        return self.__speed_x

    def get_speed_y(self):
        """This method returns- speed y."""
        return self.__speed_y

    def get_prow_direction(self):
        """This method returns- the heading of the ship in degrees."""
        return self.__prow_direction

    def set_location(self, new_x_location, new_y_location):
        """This method gets the new location for the ship and sets it."""
        self.__location_x = new_x_location
        self.__location_y = new_y_location

    def set_speed(self, new_x_speed, new_y_speed):
        """This method gets the new speed for the ship and sets it."""
        self.__speed_x = new_x_speed
        self.__speed_y = new_y_speed

    def set_prow_direction(self, new_prow_direction):
        """This method gets the new heading of the ship and sets it."""
        self.__prow_direction = new_prow_direction

    def get_radius(self):
        """This method returns the radius of the ship."""
        return self.__radius
