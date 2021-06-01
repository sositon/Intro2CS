class Board:
    """
    This class define a board object, size 7*7 with a target point.
    """

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.__width = 7
        self.__length = 7
        self.__target = 3, 7
        self.__cars = list()
        self.__grid = [["_" for c in range(self.__width)]
                       for r in range(self.__length)]
        for i in range(self.__length):
            self.__grid[i].append("E") if i == 3 else self.__grid[i].append("*")

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the __board for printing, but may not assume details about it.
        out = []
        for row in self.__grid:
            out.append(' '.join([r for r in row]))
        return '\n'.join(out)

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this __board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the __target cell (3,7)
        res = [(i, j) for i in range(len(self.__grid))
               for j in range(len(self.__grid))]
        res.append(self.target_location())
        return res

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        res = list()
        for car in self.__cars:
            for p in car.possible_moves().items():
                tmp_tuple = (car.get_name(), *p)
                movekey = tmp_tuple[1]
                cord_to_be_free = car.movement_requirements(movekey)
                if self.cell_content(*cord_to_be_free) is None:
                    res.append(tmp_tuple)
        return res

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return self.__target

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row, col = coordinate
        return self.__grid[row][col] if self.__grid[row][col] != "_" and \
                                        self.__grid[row][col] != "E" else None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        for cord in car.car_coordinates():
            if cord not in self.cell_list() or \
                    self.cell_content(cord) is not None:
                return False
        for c in self.__cars:
            if c.get_name() == car.get_name():
                return False
        for cord in car.car_coordinates():
            x, y = cord
            self.__grid[x][y] = car.get_name()
        self.__cars.append(car)
        return True

    def __move_car_help(self, name, old_list, new_list):
        """
        :param name: A str representing the name of the car on the board
        :param old_list: A list of tuples representing the old cords of the car
        :param new_list: A list of tuples representing the new cords of the car
        :return: None. erase the name of the car from the old cords and
        write the name in the new cords
        """
        for cord in old_list:
            r, c = cord
            name = self.__grid[r][c]
            self.__grid[r][c] = "_"
        for cord in new_list:
            r, c = cord
            self.__grid[r][c] = str(name)

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        for option in self.possible_moves():
            # option is a tuple of the form (name,movekey,description)
            n, k, *d = option
            if name == n and movekey == k:
                for c in self.__cars:
                    if c.get_name() == name:
                        old_cord = c.car_coordinates()
                        c.move(movekey)
                        new_cord = c.car_coordinates()
                        # check if doesn't contain negative coordinates
                        for cord in new_cord:
                            x, y = cord
                            if x < 0 or y < 0:
                                return False
                        self.__move_car_help(name, old_cord, new_cord)
                        return True
        return False
