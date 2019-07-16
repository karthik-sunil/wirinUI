from gtts import gTTS 
import os
#from pygame import mixer
#fw = open("readthis.txt", "w")
#inp = input("enter text: ")
#fw.write(inp)
#fw.close() 
f = open("readthis.txt", "r")
text = f.read()
f.close() 
language = "en-us"
gtts_obj = gTTS(text= text, lang = language, slow = False )
gtts_obj.save(r"readit.mp3")
#mixer.music.load("readit.mp3")
#mixer.music.play()
#os.system("readit.mp3")

