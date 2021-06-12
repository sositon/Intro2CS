from screen import Screen
import sys
from ship import *
from asteroid import *
from torpedo import *
from random import *
import math

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    LIFE_TITLE = "LIFE"
    LIFE_MSG = "You were hit by an asteroid, 1 life reduced"
    QUIT_TITLE = "QUIT"
    QUIT_MSG = "Thank you for playing!"
    WIN_TITLE = "WIN"
    WIN_MSG = "You won!"
    END_LIFE_MSG = "You run out of life, game over"
    INITIAL_SCORE = 0
    INITIAL_LIFE = 3
    INITIAL_SPEED_X = 0
    INITIAL_SPEED_Y = 0
    INITIAL_HEADING = 0
    END_GAME_LIFE = 0
    MAX_TORPEDOES_AMOUNT = 10
    ROTATE_DEGREE = 7
    REDUCED_ASTEROID_SIZE = 1
    REDUCED_SHIP_LIFE = 1
    ASTEROID_SPEED_LIST = [i for i in range(-4, 5) if i != 0]
    ASTEROIDS_DIC = {1: 100, 2: 50, 3: 20}  # {size: score}

    def __init__(self, asteroids_amount=DEFAULT_ASTEROIDS_NUM):
        """
        This function defines the variables we use in the game and also creates the asteroids in the game according
        to the starting conditions and the desired amount.
        """
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__score = self.INITIAL_SCORE
        self.__life = self.INITIAL_LIFE

        self.__ship = Ship(randint(self.__screen_min_x, self.__screen_max_x),
                           randint(self.__screen_min_y, self.__screen_max_y),
                           self.INITIAL_SPEED_X, self.INITIAL_SPEED_Y,
                           self.INITIAL_HEADING)

        self.__torpedoes_list = list()
        self.__asteroids_list = list()

        # init asteroids
        while len(self.__asteroids_list) < asteroids_amount:
            asteroid = Asteroid(
                randint(self.__screen_min_x, self.__screen_max_x),
                randint(self.__screen_min_y,
                        self.__screen_max_y), choice(self.ASTEROID_SPEED_LIST),
                choice(self.ASTEROID_SPEED_LIST), Asteroid.MAX_SIZE)
            if asteroid.get_location_x() != self.__ship.get_location_x() or \
                    asteroid.get_location_y() != self.__ship.get_location_y():
                self.__asteroids_list.append(asteroid)
                self.__screen.register_asteroid(asteroid, asteroid.get_size())

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def __draw_ship(self):
        """
        This function displays the ship on the game screen as a user display.
        """
        self.__screen.draw_ship(self.__ship.get_location_x(),
                                self.__ship.get_location_y(),
                                self.__ship.get_prow_direction())

    def __draw_asteroid(self):
        """
        This function displays the asteroid on the game screen as a user display.
        """
        for asteroid in self.__asteroids_list:
            self.__screen.draw_asteroid(asteroid, asteroid.get_location_x(),
                                        asteroid.get_location_y())

    def __draw_torpedo(self):
        """
        This function displays the torpedo on the game screen as a user display.
        In addition for all the torpedoes according to the defined quantity, calculate with the help of a formula
        their speed.
        """
        ship = self.__ship
        screen = self.__screen
        if screen.is_space_pressed() and \
                len(self.__torpedoes_list) < self.MAX_TORPEDOES_AMOUNT:
            torpedo = Torpedo(ship.get_location_x(), ship.get_location_y(),
                              ship.get_speed_x() + 2 *
                              math.cos(
                                  math.radians(ship.get_prow_direction())),
                              ship.get_speed_y() + 2 *
                              math.sin(
                                  math.radians(ship.get_prow_direction())),
                              ship.get_prow_direction())
            self.__torpedoes_list.append(torpedo)
            self.__screen.register_torpedo(torpedo)
            self.__screen.draw_torpedo(torpedo, torpedo.get_location_x(),
                                       torpedo.get_location_y(),
                                       torpedo.get_heading())

    def __move_objects(self, obj):
        """
        This function is the function that defines new coordinates for a particular object (ship\asteroid\torpedo)
        and returns the newly defined X coordinate and Y coordinate.
        """
        delta_x = self.__screen_max_x - self.__screen_min_x
        delta_y = self.__screen_max_y - self.__screen_min_y
        new_spot_x = self.__screen_min_x + (obj.get_location_x() +
                                            obj.get_speed_x() -
                                            self.__screen_min_x) % delta_x
        new_spot_y = self.__screen_min_y + (obj.get_location_y() +
                                            obj.get_speed_y() -
                                            self.__screen_min_y) % delta_y
        return new_spot_x, new_spot_y

    def __change_ship_direction(self):
        """
        This function change ship direction depending on the angle cut in a certain direction.
        """
        if self.__screen.is_right_pressed():
            self.__ship.set_prow_direction(self.__ship.get_prow_direction()
                                           - self.ROTATE_DEGREE)
        if self.__screen.is_left_pressed():
            self.__ship.set_prow_direction(self.__ship.get_prow_direction()
                                           + self.ROTATE_DEGREE)

    def __speed_up_ship(self):
        """
        This function uses a formula with which it calculates the speed of the ship and returns the new speed in the
        X and Y directions.
        """
        if self.__screen.is_up_pressed():
            new_speed_x = self.__ship.get_speed_x() + \
                math.cos(math.radians(self.__ship.get_prow_direction()))
            new_speed_y = self.__ship.get_speed_y() + \
                math.sin(math.radians(self.__ship.get_prow_direction()))
            return new_speed_x, new_speed_y
        return self.__ship.get_speed_x(), self.__ship.get_speed_y()

    def __divide_asteroids(self, asteroid, torpedo):
        """
        This function is responsible for handling cases where there is damage to the asteroid, in some cases the
        asteroid will divide and some parts will say different size, speed and different directions in X Y axes.
        Created following the division.
        """
        if asteroid.get_size() == 1:
            self.__screen.unregister_asteroid(asteroid)
            self.__asteroids_list.remove(asteroid)
        else:
            # calculate new speed for the asteroid
            new_speed_x = (torpedo.get_speed_x() +
                           asteroid.get_speed_x()) / math.sqrt(
                asteroid.get_speed_x() ** 2 + asteroid.get_speed_y() ** 2)
            new_speed_y = (torpedo.get_speed_y() +
                           asteroid.get_speed_y()) / math.sqrt(
                asteroid.get_speed_x() ** 2 + asteroid.get_speed_y() ** 2)
            # save asteroid attributes before division and erasing
            new_location_x = asteroid.get_location_x()
            new_location_y = asteroid.get_location_y()
            new_size = asteroid.get_size() - self.REDUCED_ASTEROID_SIZE
            self.__screen.unregister_asteroid(asteroid)
            self.__asteroids_list.remove(asteroid)
            self.__asteroids_list.append(Asteroid(new_location_x,
                                                  new_location_y,
                                                  new_speed_x,
                                                  new_speed_y,
                                                  new_size))
            self.__asteroids_list.append(Asteroid(new_location_x,
                                                  new_location_y,
                                                  -new_speed_x,
                                                  -new_speed_y,
                                                  new_size))
            asteroid_1, asteroid_2 = self.__asteroids_list[-2:]
            self.__screen.register_asteroid(asteroid_1, asteroid_1.get_size())
            self.__screen.register_asteroid(asteroid_2, asteroid_2.get_size())
        if torpedo in self.__torpedoes_list:
            self.__screen.unregister_torpedo(torpedo)
            self.__torpedoes_list.remove(torpedo)

    def __torpedoes(self):
        """
        The function is responsible for handling everything known about torpedoes, including displaying a torpedo on
        the screen, editing the score according to the game's instructions and dividing the astros if the torpedo
        hit the asteroid during the game.
        """
        for torpedo in self.__torpedoes_list:
            self.__screen.draw_torpedo(torpedo, torpedo.get_location_x(),
                                       torpedo.get_location_y(),
                                       torpedo.get_heading())
            x_torpedo, y_torpedo = self.__move_objects(torpedo)
            torpedo.set_location(x_torpedo, y_torpedo)
            # life time
            if torpedo.get_life_time() > 0:
                torpedo.set_life_time(torpedo.get_life_time() - 1)
            else:
                self.__screen.unregister_torpedo(torpedo)
                self.__torpedoes_list.remove(torpedo)
            # intersection
            for asteroid in self.__asteroids_list:
                if asteroid.has_intersection(torpedo):
                    self.__score += self.ASTEROIDS_DIC[asteroid.get_size()]
                    self.__screen.set_score(self.__score)
                    self.__divide_asteroids(asteroid, torpedo)

    def __asteroids(self):
        """
        The function is responsible for handling the asteroids, displays and deletes them from the screen display as
        needed, updates the number of lives in the game according to the asteroid collisions and moves the asteroids
        according to new positions obtained.
        """
        for asteroid in self.__asteroids_list:
            x_asteroid, y_asteroid = self.__move_objects(asteroid)
            asteroid.set_location(x_asteroid, y_asteroid)
            if self.__life > self.END_GAME_LIFE and asteroid.has_intersection(
                    self.__ship):
                self.__life -= self.REDUCED_SHIP_LIFE
                self.__screen.show_message(self.LIFE_TITLE, self.LIFE_MSG)
                self.__screen.remove_life()
                self.__screen.unregister_asteroid(asteroid)
                self.__asteroids_list.remove(asteroid)

    def __end_game(self):
        """
        This function presents all the options for ending a game - win, loss and retirement. If one of these cases
        happens the function will return True otherwise it will return False.
        """
        if not self.__asteroids_list:
            self.__screen.show_message(self.WIN_TITLE, self.WIN_MSG)
            return True
        if self.__life == self.END_GAME_LIFE:
            self.__screen.show_message(self.LIFE_TITLE, self.END_LIFE_MSG)
            return True
        if self.__screen.should_end():
            self.__screen.show_message(self.QUIT_TITLE, self.QUIT_MSG)
            return True
        return False

    def _game_loop(self):
        """
        The function is responsible for performing the various actions responsible for the course of the game, and is
        called cyclically over and over throughout the run of the game.
        """
        # TODO: Your code goes here
        self.__draw_ship()
        self.__draw_asteroid()
        self.__draw_torpedo()
        x_ship, y_ship = self.__move_objects(self.__ship)
        self.__ship.set_location(x_ship, y_ship)
        self.__change_ship_direction()
        speed_x, speed_y = self.__speed_up_ship()
        self.__ship.set_speed(speed_x, speed_y)
        self.__asteroids()
        self.__torpedoes()
        if self.__end_game():
            self.__screen.end_game()
            sys.exit()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
