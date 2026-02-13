import speech_recognition as sr

def transcribe_wav_google(wav_path: str, language: str = "en-US") -> str:
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)

    # Google Web Speech API (via SpeechRecognition)
    return r.recognize_google(audio, language=language)
