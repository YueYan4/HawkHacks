import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()


def recognize_speech_from_mic(r, mic):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        text = r.recognize_google(audio, True, language = 'en')
        print(text)

