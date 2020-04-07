from RPi import GPIO
from time import sleep

class Wheel:

    def __init__(self, sides=8):
        """
        Default constructor for wheen has 8 sides - octogon
        :param sides:
        """
        self.sides = sides
        self.spinning = False
        self.current_pos = 0

    def update_wheel_position(self, direction):
        self.spinning = True
        if direction == -1:
            self.spin_backwards()
        if direction == 1:
            self.spin_forward()

    def spin_backwards(self):
        self.current_pos -= 1
        if self.current_pos < 0:
            self.current_pos = self.sides

    def spin_forward(self):
        self.current_pos += 1
        if self.current_pos > self.sides:
            self.current_pos = 0


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
        try:
            while True:
                clk_state = GPIO.input(self.clk)
                if clk_state != self.clkLastState:
                    dt_state = GPIO.input(self.dt)
                    if dt_state != clk_state:
                        self.wheel.spin_forward()
                    else:
                        self.wheel.spin_backwards()
                    print(self.wheel.current_pos)
                self.clkLastState = clk_state
                sleep(0.01)
        finally:
            GPIO.cleanup()


def main():
    rotary = Rotary(8)
    rotary.run()


if __name__ == "__main__":
    main()



