class Car:
    """
    This class define a car object.
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        x, y = self.__location
        res = []
        for i in range(self.__length):
            if self.__orientation:
                res.append((x, y + i))
            else:
                res.append((x + i, y))
        return res

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.
        if self.__orientation:
            return {"l": "the car can drive left", "r": "the car can drive "
                                                        "right"}
        else:
            return {"u": "the car can drive up", "d": "the car can drive down"}

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        x, y = self.__location
        if movekey == "d":
            x += self.__length
        elif movekey == "u":
            x -= 1
        elif movekey == "r":
            y += self.__length
        elif movekey == "l":
            y -= 1
        return [(x, y)]

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if movekey in self.possible_moves():
            new_location_list = self.car_coordinates() + \
                                self.movement_requirements(movekey)
            new_location_list.pop(0)
            new_location = min(new_location_list)
            self.__location = new_location
            return True
        else:
            return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
