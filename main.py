import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime
import requests
import urllib.parse

# Inicializa o sintetizador de voz
voz = pyttsx3.init()
voz.setProperty('voice', voz.getProperty('voices')[-2].id)  # voz masculina

def falar(frase):
    print(f"JARVIS: {frase}")  # Também mostra no console
    voz.say(frase)
    voz.runAndWait()

def ouvir_comando():
    r = sr.Recognizer()
    r.energy_threshold = 300
    with sr.Microphone() as source:
        print("Ouvindo...")
        r.adjust_for_ambient_noise(source, duration=1)  # Ajusta ruído ambiente
        audio = r.listen(source, timeout=1000, phrase_time_limit=10)
        try:
            comando = r.recognize_google(audio, language='pt-BR')
            print("Você disse:", comando)
            return comando.lower()
        except sr.UnknownValueError:
            falar("Não entendi o que você disse.")
            return ""
        except sr.RequestError:
            falar("Erro ao se conectar ao serviço de voz.")
            return ""
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return ""

def buscar_clima(cidade):
    chave_api = "632dcc313294e4c3d593616d605e3b81"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&lang=pt_br&units=metric"

    resposta = requests.get(url)
    dados = resposta.json()

    if resposta.status_code == 200:
        temp = dados['main']['temp']
        descricao = dados['weather'][0]['description']
        clima_formatado = f"Em {cidade}, está fazendo {temp} graus com {descricao}."
        return clima_formatado
    else:
        return "Não consegui obter o clima agora."

def pesquisar_google(termo):
    termo_codificado = urllib.parse.quote_plus(termo)
    url = f"https://www.google.com/search?q={termo_codificado}"
    webbrowser.open(url)

# Loop principal
falar("JARVIS ativado. Olá, Diego.")
while True:
    comando = ouvir_comando()

    if "jarvis" in comando:

        if "horas" in comando:
            agora = datetime.now()
            falar(f"Agora são {agora.hour} horas e {agora.minute} minutos.")

        elif "abrir navegador" in comando:
            falar("Abrindo o navegador.")
            webbrowser.open("https://www.google.com")

        elif "clima" in comando:
            falar("Qual cidade você quer saber o clima?")
            cidade = ouvir_comando()
            if cidade:
                clima = buscar_clima(cidade)
                print(clima)
                falar(clima)
            else:
                falar("Não consegui ouvir a cidade.")

        elif "pesquisar" in comando:
            termo = comando.replace("jarvis", "").replace("pesquisar", "").replace("sobre", "").strip()
            if termo:
                falar(f"Pesquisando {termo} no Google.")
                pesquisar_google(termo)
            else:
                falar("O que você quer pesquisar?")
                termo = ouvir_comando()
                if termo:
                    falar(f"Pesquisando {termo} no Google.")
                    pesquisar_google(termo)
                else:
                    falar("Não consegui ouvir o termo para pesquisar.")


        elif "encerrar" in comando or "desligar" in comando:
            falar("Desligando o sistema. Até mais, Diego.")
            break

        else:
            falar("Desculpe, não entendi esse comando.")
