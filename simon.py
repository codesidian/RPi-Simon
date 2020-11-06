import RPi.GPIO as GPIO
import time, random
GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.OUT)
class LED():
    def __init__(self, channel, colour):
        self.colour = colour
        self.channel = channel
        self.is_on = False
        GPIO.setup(channel, GPIO.OUT)
    def on(self):
        self.is_on = True
        GPIO.output(self.channel, True)
    def off(self):
        self.is_on = False
        GPIO.output(self.channel, False)

#This is bad, but i'm lazy. 
buzzer = LED(24, "buzzer")

led_dict = {}
led_dict["yellow"] = LED(17, "yellow")
led_dict["green"] = LED(2, "green")
led_dict["red"] = LED(22, "red")
led_dict["blue"] = LED(27, "blue")

def play_simon(simon):
    print(f"simon:{simon}")
    for colour in simon:
        led_dict[colour].on()
        time.sleep(2)
        led_dict[colour].off()
        time.sleep(1)

def get_input(length_of_sequence):
    choices = []
    while len(choices) < length_of_sequence:
        if GPIO.input(25):
            choices.append("yellow")
            led_dict["yellow"].on()
            time.sleep(0.5)
            led_dict["yellow"].off()
        elif GPIO.input(23):
            choices.append("green")
            led_dict["green"].on()
            time.sleep(0.5)
            led_dict["green"].off()
        elif GPIO.input(15):
            choices.append("red")
            led_dict["red"].on()
            time.sleep(0.5)
            led_dict["red"].off()
        elif GPIO.input(8):
            choices.append("blue")
            led_dict["blue"].on()
            time.sleep(0.5)
            led_dict["blue"].off()
    time.sleep(0.4)
    return choices

def entry_sequence():
    for col,led in led_dict.items():
        led.on()
        time.sleep(0.5)
        led.off()

def exit_sequence():
    for i in range(5):
        for col,led in led_dict.items():
            led.on()
        time.sleep(0.5)
        for col,led in led_dict.items():
            led.off()
        time.sleep(0.5)

def all_on_off():
    for col,led in led_dict.items():
        led.on()
    time.sleep(0.5)
    for col,led in led_dict.items():
        led.off()
    time.sleep(0.5)

def play_buzzer():
    buzzer.on()
    time.sleep(0.1)
    buzzer.off()
    time.sleep(0.1)
    buzzer.on()
    time.sleep(0.1)
    buzzer.off()
    time.sleep(0.1)
    buzzer.on()
    time.sleep(0.3)
    buzzer.off()

    
def main():
    entry_sequence()
    time.sleep(0.5)
    game_over = False
    score = 0
    simon = []
    simon.append(random.choice(list(led_dict.keys())))
    print(f"simon:{simon}")
    while not game_over:
        sequence = []
        play_simon(simon)
        all_on_off()
        sequence = get_input(len(simon))
        if not sequence == simon:
            play_buzzer()
            exit_sequence()
            game_over = True
        else:
            simon.append(random.choice(list(led_dict.keys())))
        
        
        
    
game_exit = False
while not game_exit:
    main()
    game_exit = True


GPIO.cleanup()