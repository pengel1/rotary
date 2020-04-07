from RPi import GPIO
from time import sleep
import pygame
import os, random


class MusicPlayer:

    def __init__(self):
        self.__playing_music = False
        pygame.init()
        pygame.mixer.init()

    def get_random_file(self, starts_with):
        print('lisinting...')
        files = os.listdir("./sounds/")
        print('files %s' % files)
        filtered_files = list(filter(lambda k: starts_with in k, files))
        print("files are %s" % filtered_files)
        return random.choice(filtered_files)

    def play_music(self):
        if not self.__playing_music:
            try:
                # do stuff here play that music
                self.__playing_music = True
                print("Playing some music...")
                file = self.get_random_file('spinner')
                sound = pygame.mixer.Sound(file)
                pygame.mixer.Sound.play(sound)
            except Exception as e:
                print("Exception %s" % e)

    def stop_music(self):
        print('Stopping music..')
        if self.__playing_music:
            # do stuff that turns off music
            pygame.mixer.music.stop()
            file = self.get_random_file('winner')
            sound = pygame.mixer.Sound(file)
            pygame.mixer.Sound.play(sound)
            self.__playing_music = False


class Wheel:

    def __init__(self, sides=8):
        """
        Default constructor for wheen has 8 sides - octogon
        :param sides:
        """
        self.sides = sides
        self.spinning = False
        self.current_pos = 0
        self.music_player = MusicPlayer()

    def update_wheel_position(self, direction):
        self.spinning = True
        if direction == -1:
            self.spin_backwards()
        if direction == 1:
            self.spin_forward()

    def spin_backwards(self):
        self.music_player.play_music()
        self.current_pos -= 1
        if self.current_pos < 0:
            self.current_pos = self.sides

    def spin_forward(self):
        self.music_player.play_music()
        self.current_pos += 1
        if self.current_pos > self.sides:
            self.current_pos = 0

    def stop_spinning(self):
        self.music_player.stop_music()


class Rotary:

    def __init__(self, sides=8):
        self.clk = 17
        self.dt = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.counter = 0
        self.clkLastState = GPIO.input(self.clk)
        self.wheel = Wheel(sides)

    def run(self):
        has_not_moved = 0
        try:
            while True:
                clk_state = GPIO.input(self.clk)
                if clk_state != self.clkLastState:
                    dt_state = GPIO.input(self.dt)
                    has_not_moved = 1
                    if dt_state != clk_state:
                        self.wheel.spin_forward()
                    else:
                        self.wheel.spin_backwards()

                    print(self.wheel.current_pos)
                else:
                    if has_not_moved > 0 and has_not_moved > 100:
                        # test if stopped spinning stopped spinning
                        self.wheel.stop_spinning()
                        has_not_moved = 0
                    else:
                        has_not_moved += 1
                self.clkLastState = clk_state
                sleep(0.01)
        finally:
            GPIO.cleanup()


def main():
    rotary = Rotary(8)
    rotary.run()
    #m = MusicPlayer()
    #m.play_music()


if __name__ == "__main__":
    main()



