import sys
sys.path.append('../')
import rgb1602
import RPi.GPIO as GPIO
import time



clk = 18
dt = 23
sw = 24
cs = 4 #chip select pin
# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP) #clk
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP) #dt
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP) #sw
#initalizing variables
previousValue = 1
resistance = 0
lcd=rgb1602.RGB1602(16,2)
pot_num = 0
potIs = 0
prev_time = time.time()

#this function is when you are actively selecting the value you want to upload to the potentiometer
def rotary_active():
    global previousValue
    global resistance
    global prev_time
    current_time = time.time()
    if previousValue != GPIO.input(clk):            #this is to poll the rotary encoder to check if anything is changed so it is not always running through the code.
        if GPIO.input(clk) == 0:                    #if clk is open prior to dt than you know the knob is being spun anti clockwise and can update values accordingly
            if GPIO.input(dt) == 0:
                direction = "anti-clockwise"
                speed = current_time - prev_time
                if speed < .2:                      #speed is to test how fast the knob is spinning this is just recorded from current time to last time the knob was spun
                    if (resistance - 100) > 100:    
                        resistance -= 100
                    else:
                        resistance = 100
                elif (resistance - 10) > 100:
                    resistance -= 10
                else:
                    resistance = 100
                print(f"Direction: {direction}, Resistance: {resistance}, Speed: {speed}")      #this shows what direction the user spun the knob the new resistance value and how fast the spin was this if for debugging
                lcd.clear()
                lcd.setCursor(0, 0)                     #cursor requires a row and column number for the display this just says start from top left
                lcd.printout(f"Select with knob")       #print to display
                lcd.setCursor(0, 1)                     #cursor points to second row
                lcd.printout(f"{resistance} ohms")      #print to display
                time.sleep(.1)                          #This is for a debounce so the rotary encoder is not double reading or reading backwards. 
                prev_time = current_time                #update time
            else:                                       #this is to show dt was before clk meaning this part of the function is for clock wise everything below is the same as above but calculated for going clockwise instead of anti clockwise
                direction = "clockwise"
                speed = current_time - prev_time
                if speed < .2:
                    if (resistance + 100) < 10000:
                        resistance += 100
                    else:
                        resistance = 10000
                elif (resistance + 10) < 10000:
                    resistance += 10
                else:
                    resistance = 10000
                print(f"Direction: {direction}, Resistance: {resistance}, Speed: {speed}")
                lcd.clear()
                lcd.setCursor(0, 0)         
                lcd.printout(f"Select with knob")
                lcd.setCursor(0, 1)
                lcd.printout(f"{resistance} ohms")
                time.sleep(.1)
                prev_time = current_time                
        previousValue = GPIO.input(clk)                 #update previous value for polling so you can retest if something has changed

#this function is for the user to select which potentiometer they would like to be updating the values for
def pot_select():
    global previousValue
    global pot_num
    global potIs
    global count
    if previousValue != GPIO.input(clk):                            #same polling method as above 
        if (GPIO.input(clk) == 0) or (GPIO.input(dt) == 0):         #becasue there is only two options no need to determine direction, we can just say switch to other pot
            if pot_num == 0:
                pot_num = 1
            else:
                pot_num = 0
            print(f"Selected pot: {pot_num}")
            if pot_num == 1:
                lcd.setCursor(0,1)                              #Points to the first option in the display which is pot P0
                lcd.blink()                                     #this is for showing the user what pot they are going to choose
            else:
                lcd.setCursor(3,1)                              #Points to the second option in the display which is pot P1
                lcd.blink()                                     #this is for showing the user what pot they are going to choose
            time.sleep(.1)
    if GPIO.input(sw) == 0:                                     #checks if user has selected pot by clicking the rotary encoder
        print(f"Final selected pot is: {pot_num}")              #prints to console for debugging
        lcd.clear()                                             #dispaly clear
        lcd.setCursor(0, 0)                                     
        lcd.printout(f"Select with knob")                       #display for updating pot which runs after this function
        lcd.setCursor(0, 1)
        lcd.printout(f"{resistance} ohms")                      #prints current resistance and ohms 
        potIs = 1
        count = 1
        time.sleep(.5)                                          #delay for debounce
    previousValue = GPIO.input(clk)                             #polling again


while True:
    resistance = 100                                            #declaring resistance to automaticlly be in our bounds by intalizing it to 100 
    pot_num = 0                                                 #setting pot selected to one intially to be in the bounds of the code
    lcd.setRGB(255,100,0)                                       #sets the color of the dispaly
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout(f"Select pot:")                                #starts the display for the user to select pot once the program starts and clears once it restarts
    lcd.setCursor(0, 1)
    lcd.printout(f"P0")                                         #dispaly PO
    lcd.setCursor(3, 1)
    lcd.printout(f"P1")                                         #dispaly P1
    lcd.setCursor(0,1)                                          #intialize the blink method to be on P0 which is what was intalized
    lcd.blink()                                             
    while (potIs == 0):                                         #potIs is the pot we will write to after being selected
        pot_select()                                            #calls pot_select function
    prev_time = time.time()
    while count == 1:
        rotary_active()                                         #calls function rotary_active
        prev_time2 = time.time()
        while GPIO.input(sw) == 0:
            if (prev_time2 - time.time()) < -3:
                print(f"Exited")
                time.sleep(.1)
                pot_num = 0
                count = 0
                potIs = 0
            else:
                print(f"Selected resistance is : {resistance}, This resistance is being applied to : {pot_num}")
                lcd.clear()
                lcd.setCursor(0, 0)
                lcd.printout(f"Resistance on: {pot_num}")
                lcd.setCursor(0, 1)
                lcd.printout(f"{resistance} ohms")
                #insert resistance and upload it to the pot #
                time.sleep(3)
      
     
