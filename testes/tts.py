import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Fale alguma coisa:")
    audio = r.listen(source)

try:
    texto = r.recognize_google(audio, language='pt-BR')
    print(f"Você disse: {texto}")
except Exception as e:
    print(f"Erro: {e}")
