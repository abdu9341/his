import pyttsx3


def speech(name, department, patient_id):

    engine = pyttsx3.init()

    voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_arSA_NaayfM'

    engine.setProperty('voice', voice_id)

    engine.setProperty('rate', 140)  # 设置语速
    engine.setProperty('volume', 0.7)  # 设置音量

    # 语音播放
    text1 = 'إلى العيادة'
    textToAudio = name + text1 + department

    path = "C:/his/media/calling/"f'{patient_id}.mp3'

    engine.save_to_file(textToAudio, path)
    engine.runAndWait()
