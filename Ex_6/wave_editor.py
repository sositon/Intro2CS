from wave_helper import *
import math
import os

# Constants
SOUND_REVERSE = 1
SOUND_NEGATE = 2
SOUND_ACCELERATE = 3
SOUND_SLOW = 4
SOUND_AMPLIFY = 5
SOUND_REDUCE = 6
SOUND_DIM = 7
EXIT_EDIT_MENU = 8

LEFT_CHANNEL = 0
RIGHT_CHANNEL = 1
MIN_VOLUME = -32768
MAX_VOLUME = 32767
SAMPLE_RATE = 2000
SILENCE = 'Q'

EDIT_MENU = '1'
COMPOSING_MENU = '2'
END_MENU = '3'


def sound_reverse(data_list):
    """
    :param data_list: list of lists holds the audio data
    :return: the reversed audio data
    """
    return list(reversed(data_list))


def sound_negate(data_list):
    """
    :param data_list: list of lists holds the audio data
    :return: the negative audio data
    """
    data_list = [[-i for i in sample] for sample in data_list]
    for sample in data_list:
        if abs(MIN_VOLUME) in sample:
            if sample[LEFT_CHANNEL] == abs(MIN_VOLUME):
                sample[LEFT_CHANNEL] = MAX_VOLUME
            else:
                sample[RIGHT_CHANNEL] = MAX_VOLUME
    return data_list


def sound_accelerate(data_list):
    """
    :param data_list: list of lists holds the audio data
    :return: half of the audio data
    """
    return [i for i in data_list[::2]]


def sound_slow(data_list):
    """
    :param data_list: list of lists holds the audio data
    :return: a new audio list contain the average of every two adjacent cells
    """
    result_list = []
    average_list = [[average(sample[i], sample[i + 1]) for i in
                     range(len(sample) - 1)] for sample in zip(*data_list)]
    average_list = list(zip(*average_list))[::-1]
    data_list = data_list[::-1]
    for j in range(2 * len(data_list) - 1):
        if j % 2 == 0:
            result_list.append(data_list.pop())
        else:
            result_list.append(list(average_list.pop()))
    return result_list


def sound_amplify(data_list):
    """
    :param data_list: list of lists holds the audio data
    :return: the increased volume audio data
    """
    amplify_list = [[int(i * 1.2) for i in sample] for sample in data_list]
    for i in amplify_list:
        if i[LEFT_CHANNEL] > MAX_VOLUME:
            i[LEFT_CHANNEL] = MAX_VOLUME
        if i[LEFT_CHANNEL] < MIN_VOLUME:
            i[LEFT_CHANNEL] = MIN_VOLUME
        if i[RIGHT_CHANNEL] > MAX_VOLUME:
            i[RIGHT_CHANNEL] = MAX_VOLUME
        if i[RIGHT_CHANNEL] < MIN_VOLUME:
            i[RIGHT_CHANNEL] = MIN_VOLUME
    return amplify_list


def sound_reduce(data_list):
    """
    :param data_list: list of lists holds the audio data
    :return: the decreased volume audio data
    """
    return [[int(i / 1.2) for i in sample] for sample in data_list]


def average(a, b, c=None):
    """
    :return: the int average of 2 or 3 numbers
    """
    if c is None:
        return int((a + b) / 2)
    return int((a + b + c) / 3)


def sound_dim(data_list):
    """
    :param data_list: list of lists holds the audio data
    :return: the dimmed audio data based on the average of 3 adjacent cells
    """
    result_list = []
    last_i = len(data_list) - 1
    for i in range(len(data_list)):
        # First
        if i == 0:
            # len = 1
            if i == last_i:
                return data_list
            x = average(data_list[i][LEFT_CHANNEL],
                        data_list[i + 1][LEFT_CHANNEL])
            y = average(data_list[i][RIGHT_CHANNEL],
                        data_list[i + 1][RIGHT_CHANNEL])
        # Last
        elif i == last_i:
            x = average(data_list[last_i - 1][LEFT_CHANNEL],
                        data_list[last_i][LEFT_CHANNEL])
            y = average(data_list[last_i - 1][RIGHT_CHANNEL],
                        data_list[last_i][RIGHT_CHANNEL])
        else:
            x = average(data_list[i - 1][LEFT_CHANNEL],
                        data_list[i][LEFT_CHANNEL],
                        data_list[i + 1][LEFT_CHANNEL])
            y = average(data_list[i - 1][RIGHT_CHANNEL],
                        data_list[i][RIGHT_CHANNEL],
                        data_list[i + 1][RIGHT_CHANNEL])
        result_list.append([x, y])
    return result_list


def read_composition_file(comp_file_name):
    """
    :param comp_file_name: text file that the user enter to the program
    :return: list with all the data of the text file, without spaces and new lines
    """
    with open(comp_file_name) as comp_file:
        list_input = comp_file.read().splitlines()
    for i, item in enumerate(list_input):
        list_input[i] = item.split(" ")
        list_input[i] = [x for x in list_input[i] if x]
    return sum(list_input, [])


def edit_menu(wave_file):
    """
    :param wave_file: a tuple of length 2 contain (sample_rate, audio_data)
    :return: None. call end_menu function to save the file
    """
    data_list = wave_file[1]
    while True:
        try:
            choice = int(input("~~~~ WELCOME TO THE EDITOR MENU\n"
                               "~~~~ PLEASE ENTER THE NUMBER OF YOUR OPTION\n"
                               "~~~~ 1. REVERSE SOUND\n"
                               "~~~~ 2. NEGATE SOUND\n"
                               "~~~~ 3. ACCELERATE SOUND\n"
                               "~~~~ 4. SLOW SOUND\n"
                               "~~~~ 5. AMPLIFY SOUND\n"
                               "~~~~ 6. REDUCE SOUND\n"
                               "~~~~ 7. DIM SOUND\n"
                               "~~~~ 8. END_MENU\n"))
        except ValueError:
            print("YOUR INPUT SHOULD BE NUMBERS FROM 1-8\n")
            continue

        if choice is SOUND_REVERSE:
            data_list = sound_reverse(data_list)
            print("~~~~ REVERSED SUCCESSFULLY ~~~~\n")
        elif choice is SOUND_NEGATE:
            data_list = sound_negate(data_list)
            print("~~~~ NEGATED SUCCESSFULLY ~~~~\n")
        elif choice is SOUND_ACCELERATE:
            data_list = sound_accelerate(data_list)
            print("~~~~ ACCELERATED SUCCESSFULLY ~~~~\n")
        elif choice is SOUND_SLOW:
            data_list = sound_slow(data_list)
            print("~~~~ SLOWED SUCCESSFULLY ~~~~\n")
        elif choice is SOUND_AMPLIFY:
            data_list = sound_amplify(data_list)
            print("~~~~ AMPLIFIED SUCCESSFULLY ~~~~\n")
        elif choice is SOUND_REDUCE:
            data_list = sound_reduce(data_list)
            print("~~~~ REDUCED SUCCESSFULLY ~~~~\n")
        elif choice is SOUND_DIM:
            data_list = sound_dim(data_list)
            print(" ~~~~ DIMMED SUCCESSFULLY ~~~~\n")
        elif choice is EXIT_EDIT_MENU:
            end_menu(wave_file[0], data_list)
            break
        else:
            print("INVALID INPUT PLEASE TRY AGAIN")


def list_to_tuples(lst):
    """
    :param lst: a list
    :return: a list of tuples
    """
    list_of_tuples = []
    for i in range(0, len(lst), 2):
        list_of_tuples.append((lst[i], int(lst[i + 1])))
    return list_of_tuples


def ask_for_composition_file():
    """ gets an input from the user and check if it's valid
    :return: the composing file name
    """
    while True:
        composition_file_name = input("ENTER THE COMPOSITION FILE NAME YOU "
                                      "WANT TO LOAD\n")
        if not os.path.isfile(composition_file_name):
            print("FILE DOESN'T EXIST")
        else:
            return composition_file_name


def composing_menu(data_list):
    """
    :param data_list: list of tuples contain (char, play_time)
    :return: list of lists holds the audio data based on the data list we've got
    """
    melody_compose = []
    note_list = list_to_tuples(data_list)
    char_dic = {'A': 440, 'B': 494, 'C': 523, 'D': 587, 'E': 659, 'F': 698,
                'G': 784}
    for note in range(len(note_list)):
        char, play_time = note_list[note]
        if char == SILENCE:
            sample_sound = play_time * 125
            samples_per_cycle = 0
        else:
            frequency_rate = char_dic[char]
            sample_sound = play_time * 125
            samples_per_cycle = SAMPLE_RATE / frequency_rate

        for i in range(sample_sound):
            if samples_per_cycle != 0:
                value = int(MAX_VOLUME * math.sin(
                    (2 * math.pi) * i / samples_per_cycle))
                melody_compose += [[value, value]]
            else:
                melody_compose += [[0, 0]]
    return melody_compose


def ask_for_wave_file():
    """
    :return: the wave file tuple (sample_rate, audio_data)
    """
    wave_file_name = input("ENTER THE WAVE FILE NAME YOU WANT TO LOAD\n")
    wave_file = load_wave(wave_file_name)
    while not isinstance(wave_file, tuple):
        wave_file_name = input("TRY AGAIN\n")
        wave_file = load_wave(wave_file_name)

    return wave_file


def check_input(choice):
    """
    :param choice: an input
    :return: true if it's match the conditions
    """
    flag = False
    if choice == EDIT_MENU or choice == COMPOSING_MENU or choice == END_MENU:
        flag = True
    return flag


def end_menu(sample_rate, data_list):
    """
    :param sample_rate: sample rate of the file we want to save
    :param data_list: list of lists holds the audio data
    :return: None. save the file based on the user input
    """
    output_name = input("PLEASE ENTER THE NAME YOU WANT TO SAVE THE FILE AS\n")
    result = save_wave(sample_rate, data_list, output_name)
    while result:
        output_name = input("TRY AGAIN\n")
        result = save_wave(sample_rate, data_list, output_name)


def main_menu():
    """
    :return: None. the flow of the program
    """
    flag = True
    while flag:
        choice = input("WELCOME! \nPRESS 1 FOR EDITING WAVE FILE \n"
                       "PRESS 2 FOR COMPOSING A MELODY \n"
                       "PRESS 3 FOR EXIT \n")
        if check_input(choice):
            if choice == EDIT_MENU:
                edit_menu(ask_for_wave_file())
            elif choice == COMPOSING_MENU:
                file_name = ask_for_composition_file()
                data_list = composing_menu(read_composition_file(file_name))
                edit_menu((SAMPLE_RATE, data_list))
            elif choice == END_MENU:
                flag = False
        else:
            print("TRY AGAIN")


if __name__ == '__main__':
    main_menu()
