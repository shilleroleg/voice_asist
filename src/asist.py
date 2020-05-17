import os
import time
import speech_recognition as sr
import pyttsx3
from fuzzywuzzy import fuzz
import datetime

# 0. Установить requirements.txt
# 1. Установить голоса из add-on/RHVoice-v0.4-a2-setup.exe
# 2. Установить PyAudio из папки add-on. Из pypi устанавливается с ошибкой
# 3. Установить python-Levenshtein из папки add-on.

opts = {
    "alias": ('кеша', 'инокентий', 'иннокентий', 'кешан'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час', 'времени'),
        "radio": ('включи музыку', 'включи радио')
    }
}


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        # Если обращаемся к помошнику
        if voice.startswith(opts["alias"]):
            cmd = voice

            # Удаляем обращение к помошнику
            for x in opts["alias"]:
                cmd = cmd.replace(x, "").strip()

            # Удаляем вводные слова
            # Остается чистая команда
            for x in opts["tbr"]:
                cmd = cmd.replace(x, "").strip()

            # распзнаем и выполняем команду
            cmd = recognizer_cmd(cmd)
            execute_cmd(cmd['cmd'])
    except sr.UnknownValueError:
        print("[log] Голос не распознан")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка. Проверьте интернет")


def recognizer_cmd(cmd):
    rc = {'cmd': "",
          'percent': 0}

    # Нечетко сравниваем полученную команду
    # со всеми вариантами из ячейки настроек cmds
    for c, v in opts["cmds"].items():
        # Оставляем самую подходящую из всех
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd):
    if cmd == 'ctime':
        # Сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'radio':
        speak("Нужно добавить радио в настройки")

    else:
        str_else = "Команда не распознана, повторите"
        print(str_else)
        speak(str_else)


# Запуск
rec = sr.Recognizer()
mic = sr.Microphone(device_index=1)
with mic as source:
    rec.adjust_for_ambient_noise(source)  # Слушает фон чтобы отличать фон от речи
    # audio = rec.listen(source)

speak_engine = pyttsx3.init()

voices = speak_engine.getProperty('voices')
# voice_id = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\TokenEnums\\RHVoice\\Aleksandr'
speak_engine.setProperty('voice', voices[4].id)

# Произноим приветственные фразы
speak("Добрый день")
speak("Кеша слушает")

# Начинаем слушать микрофон в фоне
start_listening = rec.listen_in_background(mic, callback)

while True:
    time.sleep(0.1)
    # callback
