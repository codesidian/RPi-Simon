import RPi.GPIO as GPIO
import time, random
import contextlib

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

def buzz(noteFreq, duration):
    halveWaveTime = 1 / (noteFreq * 2 )
    waves = int(duration * noteFreq)
    for i in range(waves):
       GPIO.output(24, True)
       time.sleep(halveWaveTime)
       GPIO.output(24, False)
       time.sleep(halveWaveTime)   

def play_sound(sound):
    duration = 0.20
    if sound == "yellow":
        buzz(783.99, duration)
    elif sound == "green":
        buzz(659.25, duration)
    elif sound == "red":
        buzz(523.25, duration)
    elif sound == "blue":
        buzz(392, duration)

 
def play_simon(simon):
    print(f"simon:{simon}")
    if len(simon) > 12:
        duration = 0.1
    elif len(simon) > 7:
        duration = 0.2
    elif len(simon) > 4:
        duration = 0.3
    else:
        duration = 0.5
    for colour in simon:
        led_dict[colour].on()
        play_sound(colour)
        time.sleep(duration)
        led_dict[colour].off()
        time.sleep(duration/2)
        
def play_fail():
    t=0
    notes=[116.54,110.00,103.83,98.00,90,98.00,106]
    duration=[0.25,0.25,0.25,0.2,0.1,0.2,0.1]
    for n in notes:
        buzz(n, duration[t])
        time.sleep(duration[t] *0.1)
        t+=1
        
def get_input(simon):
    choices = []
    while len(choices) < len(simon):
        if GPIO.input(25):
            colour = "yellow"
            choices.append(colour)
            led_dict[colour].on()
            play_sound(colour)
            time.sleep(0.25)
            led_dict[colour].off()
        elif GPIO.input(23):
            colour = "green"
            choices.append(colour)
            led_dict[colour].on()
            play_sound(colour)
            time.sleep(0.25)
            led_dict[colour].off()
        elif GPIO.input(15):
            colour = "red"
            choices.append(colour)
            led_dict[colour].on()
            play_sound(colour)
            time.sleep(0.25)
            led_dict[colour].off()
        elif GPIO.input(8):
            colour = "blue"
            choices.append(colour)
            led_dict[colour].on()
            play_sound(colour)
            time.sleep(0.25)
            led_dict[colour].off()
        for chosen_colour,simons_colour in zip(choices,simon):
            if chosen_colour != simons_colour:
                return []
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
        sequence = get_input(simon)
        all_on_off()
        if not sequence == simon:
            play_fail()
            exit_sequence()
            game_over = True
        else:
            new_colour = random.choice(list(led_dict.keys()))
            # True random can produce unfun sequences. So try to come up with a different colour but with a chance of still allowing them. 
            if simon[-1] == new_colour:
                new_colour = random.choice(list(led_dict.keys()))
            simon.append(new_colour)
        
        
    
game_exit = False
while not game_exit:
    main()
    game_exit = False


GPIO.cleanup()