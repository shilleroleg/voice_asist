import time
import speech_recognition as sr
import pyttsx3
from fuzzywuzzy import fuzz
import datetime
import parse_bash

# 0. Установить requirements.txt
# 1. Установить голоса из add-on/RHVoice-v0.4-a2-setup.exe
# 2. Установить PyAudio из папки add-on. Из pypi устанавливается с ошибкой
# 3. Установить python-Levenshtein из папки add-on.


opts = {
    "alias": ('кеша', 'инокентий', 'иннокентий', 'кешан'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'который', 'включи'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'час', 'времени'),
        "radio": ('музыку', 'радио'),
        "joke": ("анекдот", "шутку", "прикол")
    }
}

# Инициализируем голосовой движок
speak_engine = pyttsx3.init()
voices = speak_engine.getProperty('voices')
# voice_id = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\TokenEnums\\RHVoice\\Aleksandr'
speak_engine.setProperty('voice', voices[4].id)


# Функция на вход принимает строку и проговаривает ее
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


# Произноим приветственные фразы
speak("Добрый день")
speak("Кеша слушает")


# Функция по нечеткому распознованию команд
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


# основная функция, которая прослушивает микрофон, переводит голос в текст, вычленяет команду
# и запускает на выполнение распознавалку команд
def command():
    # Запуск
    rec = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    with mic as source:
        rec.pause_threshold = 1
        rec.adjust_for_ambient_noise(source, duration=1)  # Слушает фон чтобы отличать фон от речи
        audio = rec.listen(source)

    cmd = []
    try:
        voice = rec.recognize_google(audio, language="ru-RU").lower()
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

            print("[log] Команда: " + cmd)
            # распознаем и выполняем команду
            cmd = recognizer_cmd(cmd)
    except sr.UnknownValueError:
        print("[log] Голос не распознан")
        cmd = command()
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка." + str(e))

    return cmd


# Функция в которой прописаны действия на ту или иную команду
def execute_cmd(cmd):
    if len(cmd) > 0:
        cmd = cmd['cmd']
    else:
        return
    if cmd == 'ctime':
        # Сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'radio':
        speak("Нужно добавить радио в настройки")
    elif cmd == 'joke':
        joke_str = parse_bash.get_joke()
        speak(joke_str)

    else:
        str_else = "Команда не распознана, повторите"
        print(str_else)
        speak(str_else)


# Бесконечный цикл на вызов функции прослушивания микрофона и выполнения команд
while True:
    time.sleep(1)
    execute_cmd(command())
