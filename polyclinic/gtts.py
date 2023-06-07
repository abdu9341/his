from gtts import gTTS
import os
# from playsound import playsound

myText = '''ben seni seviyorum'''
language = 'tr'
# arabic: ar, english: en, turkish: tr, Uyghur: ug

myObj = gTTS(text=myText, lang=language, slow=False)

myObj.save("welcome.mp3")

os.system("start welcome.mp3")

# playsound("welcome.mp3")
