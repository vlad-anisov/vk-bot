import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType 
import speech_recognition as sr
import requests
import subprocess

token = "YOUR TOKEN"

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session,176174449)

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.obj.attachments != [] and event.object.attachments[0]["type"] == "audio_message":
                request = requests.get(event.obj.attachments[0]["audio_message"]["link_mp3"])
                
                with open('voice.mp3', 'wb') as file:
                    file.write(request.content)
                subprocess.call(['ffmpeg', '-y', '-i', 'voice.mp3','voice.wav'])    

                r = sr.Recognizer() 
                with sr.AudioFile("voice.wav") as source:
                    audio = r.record(source)

                text = r.recognize_google(audio, language="ru-RU")
                id = event.obj.peer_id
                vk.messages.send(peer_id=id, random_id=0, message=text)
    except Exception:
        pass