import speech_recognition as sr

# cria um reconhecedor de voz
r = sr.Recognizer()

# abrir o microfone para captura
with sr.Microphone() as source:

    audio = r.listen(source) # define microfone como fonte de áudio


    print(r.recognize_google(audio, language='pt-BR'))

