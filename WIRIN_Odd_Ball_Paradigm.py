import random
import pygame
import time
import csv
import datetime

pygame.init()
win = pygame.display.set_mode((500, 500))
precision = 50 # Dynamic variable
beat_sl_no = 0
path = "E:\\Coding\\Wirin\\wirinUI\\tones\\"


with open(path+ r'write.csv', 'w+', newline = '') as writeFile:
    writer = csv.writer(writeFile, delimiter = ',')
    row = []
    row.append("Experiment: Odd Ball Expt")
    writer.writerow(row)
    row = []
    row.append("Normal sound: 500 Hz")
    writer.writerow(row)
    row = []
    row.append("Odd sound: 1000 Hz")
    writer.writerow(row)
    row = []
    row.append("Marker for normal sound: 5")
    writer.writerow(row)
    row = []
    row.append("Marker for odd sound: 7")
    writer.writerow(row)
    row = []
    row.append("Marker for correct click: 1")
    writer.writerow(row)
    row = []
    row.append("Marker for incorrect click: 0")
    writer.writerow(row)

    row = []
    row.append(" ")
    writer.writerow(row)
    
    #Table 
    row = []
    row.append("Sound")
    row.append("Response")
    row.append("Result")
    writer.writerow(row)
    
    row = []
    row.append("5")
    row.append("CLick")
    row.append("0")
    writer.writerow(row)
    
    row = []
    row.append("5")
    row.append("No CLick")
    row.append("1")
    writer.writerow(row)
    
    row = []
    row.append("7")
    row.append("CLick")
    row.append("1")
    writer.writerow(row)
    
    row = []
    row.append("7")
    row.append("No CLick")
    row.append("0")
    writer.writerow(row)
    
    
    row = []
    row.append(" ")
    writer.writerow(row)
    
    row = []        #Get column headers
    row.append("Sl No")
    row.append("Sound Present Time")
    row.append("Beat Type")
    row.append("Response Type")
    row.append("Key Press Time")
    row.append("Response Time")
    
    writer.writerow(row)
    
    while(1):
        
        beat_sl_no += 1
        row = []
        
        print('Delay 1 Start 2000')
        pygame.time.delay(2000)
        diff_4 = random.randint(1, precision) # Difference after 4 seconds
    
        beep_time = (int(2000*diff_4/precision))
        print('Delay 2 Start', beep_time)
        pygame.time.delay(beep_time)
        choose_sound = (random.randint(1, 10) <= 5)   # Generate 80% probability
        
        if(choose_sound == False):
            
            # "Odd Ball"
            beat_type = 7 
            pygame.mixer.music.load(path+r"500hz.wav")
            pygame.mixer.music.play(0)        
            sound_present_time = datetime.datetime.now().time()
            
            # Store the time at which the beat occurs            
            start = time.time() 
            flag = True
            break_flag = False
            while(1):
                pygame.event.get()
                mouse_status = (pygame.mouse.get_pressed())    # Check if LMB has been clicked
    
                if(time.time() - start >= 2):   #  If the driver doesn't click a mouse button in 2 seconds
                    sound_response_time = datetime.datetime.now().time()
                    response_time = 2   
                    response_type = 0 # "Incorrect"
                    break
                
                if(mouse_status[0] == 1):             # If the driver clicks a mouse button, a correct repsonse has to be registered
                    response_time = time.time() - start
                    sound_response_time = datetime.datetime.now().time()
                    response_type = 1 # "Correct"
                    print("Correct")
                    flag = False
                    break
                
                if(mouse_status[2] == 1):   # Exit
                    break_flag = True
                    break
                
            if(break_flag == True):
                break
                
            if(flag == True):
                print("Missed the beep")
                
        else:
            beat_type = 5 #"Normal"
            pygame.mixer.music.load(path+r"1000hz.wav")
            pygame.mixer.music.play(0)        
            start = time.time()
            sound_present_time = datetime.datetime.now().time()
            break_flag = False
            
            while(1):
                
                pygame.event.get()
                mouse_status = (pygame.mouse.get_pressed())    
               
                if(time.time() - start >= 2):
                    sound_response_time = datetime.datetime.now().time()
                    response_time = 2
                    response_type = 1 # "Correct"
                    break
                
                if(mouse_status[0] == 1):   # If the driver clicks a mouse button, an incorrect repsonse has to be registered
                    response_time = time.time() - start
                    sound_response_time = datetime.datetime.now().time()
                    response_type = 0 # "Incorrect"
                    print("Incorrect")
                    break
                
                if(mouse_status[2] == 1):   #Exit Wondow
                    break_flag = True
                    break
                
            if(break_flag == True):
                break
        #a = time.time()
        time1 = []
        for i in str(sound_present_time):
            if(i == ':'):
                time1.append('.')
            else:
                time1.append(i)
        
        time2 = []
        for i in str(sound_response_time):
            if(i == ':'):
                time2.append('.')
            else:
                time2.append(i)
        
        row.append(beat_sl_no)
        row.append(''.join(time1))
        row.append(beat_type)
        row.append(response_type)
        row.append(''.join(time2))
        row.append(response_time)
        writer.writerow(row)
    pygame.quit()    
writeFile.close()
