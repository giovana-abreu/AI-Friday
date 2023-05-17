from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import os
from pytube import YouTube
import youtube_dl as yt
import pyttsx3
import datetime
import webbrowser
import requests
import random
from googletrans import Translator
import pyjokes

# Iniciar Sexta

reconhecedor = sr.Recognizer()
sexta = pyttsx3.init()
sexta.setProperty('rate', 150)
sexta.setProperty('volume', 1)

# Função de inicialização da Sexta-feira

def inicia_sexta():
    with sr.Microphone() as mic:
        print('Mic On')
        reconhecedor.adjust_for_ambient_noise(mic)
        audio = reconhecedor.record(mic, duration=10, offset=None)
        texto = reconhecedor.recognize_google(audio, language='pt')
        init = ['OK SEXTA-FEIRA', 'SEXTA-FEIRA']
        if texto.upper() in init:
            audio = "Como posso ajudá-lo, senhor Stark?"
            sexta.say(audio)
            print(audio)
            sexta.runAndWait()
            return True
    return False

def sexta_escuta():
    try:
        with sr.Microphone() as mic:
            print('Mic On')
            reconhecedor.adjust_for_ambient_noise(mic)
            audio = reconhecedor.record(mic, duration=10, offset=None)
            comando = reconhecedor.recognize_google(audio, language='pt')
            comando = comando.upper()
            print(comando)
            return comando
    except Exception as err:
        sexta.say(f'Desculpe, não entendi')
        print(f'Desculpe, não entendi: {err}.')
        sexta.runAndWait()
        return ''

def cadastrar_evento():
    sexta.say("Qual evento devo cadastrar?")
    print("Qual evento devo cadastrar?")
    sexta.runAndWait()
    print("Qual evento devo cadastrar?")
    evento = sexta_escuta()
    with open('agenda.txt', 'a') as cad:
        cad.write("- " + evento + "\n")
        sexta.say("Evento cadastrado com sucesso!")
        print("Evento cadastrado com sucesso!")
        sexta.runAndWait()

def leitura_agenda():
    with open('agenda.txt', 'r') as arquivo:
        conteudo = arquivo.read()
        sexta.say(conteudo)
        sexta.runAndWait()
        print(conteudo)
        
def buscar_video(query):
    ydl_opts = {
        'default_search': 'ytsearch',
        'format': 'best',
        'noplaylist': True,
        'quiet': True
    }

    with yt.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
        if 'entries' in result:
            # Obter a URL do vídeo da primeira música encontrada
            video_url = result['entries'][0]['webpage_url']
            return video_url

    return None

def baixar_musica():
    reconhecedor = sr.Recognizer()
    microfone = sr.Microphone()
    play = pyttsx3.init()
    play.setProperty('rate', 150)
    play.setProperty('volume', 1)

    with microfone as mic:
        reconhecedor.adjust_for_ambient_noise
        play.say("Qual música deseja procurar?")
        play.runAndWait()
        audio = reconhecedor.listen(mic)
        texto = reconhecedor.recognize_google(audio, language='auto')
        musica = reconhecedor.recognize_google(audio, language='en')
        play.say(f'Buscando {musica}')
        play.runAndWait()
        
    song_name = musica
    video_url = buscar_video(song_name)

    # Baixar a música
    yt = YouTube(str(video_url))
    video = yt.streams.filter(only_audio=True).first()
    destination = str(("."))
    out_file = video.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    os.system(f'start "" "{new_file}"')

def pesquisa_web():
    sexta.say("O que você quer pesquisar?")
    sexta.runAndWait()
    print("O que você quer pesquisar?")
    with sr.Microphone() as mic:
        print('Mic On')
        reconhecedor.adjust_for_ambient_noise(mic)
        audio = reconhecedor.record(mic, duration=10, offset=None)
        try:
            pesquisa_reconhecida = reconhecedor.recognize_google(audio, language='pt')
            url = f"https://www.google.com/search?q={pesquisa_reconhecida}"
            webbrowser.open(url)
        except sr.UnknownValueError:
            print("Não foi possível reconhecer a fala.")
        except sr.RequestError:
            print("Erro ao se comunicar com o serviço de reconhecimento de fala.")


def obter_cotacao_dolar():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    cotacao = data["rates"]["BRL"]
    resposta = f"A cotação do dólar é {cotacao:.2f} reais"
    sexta.say(resposta)
    print(resposta)
    sexta.runAndWait()
    
def calculadora():
    operacoes_validas = {
        'SOMA': '+',
        'SUBTRAÇÃO': '-',
        'MULTIPLICAÇÃO': '*',
        'DIVISÃO': '/'
    }

    with sr.Microphone() as mic:
        sexta.say('Qual operação você deseja fazer?')
        print('Qual operação você deseja fazer?')
        sexta.runAndWait()
        print('Mic On')
        reconhecedor.adjust_for_ambient_noise(mic)
        audio = reconhecedor.record(mic, duration=10, offset=None)
        operacao = reconhecedor.recognize_google(audio, language='pt').upper()

        if operacao not in operacoes_validas:
            return "Operação inválida."

        sexta.say('Diga o primeiro valor')
        print('Diga o primeiro valor')
        sexta.runAndWait()
        print('Mic On')
        reconhecedor.adjust_for_ambient_noise(mic)
        audio = reconhecedor.record(mic, duration=10, offset=None)
        a = float(reconhecedor.recognize_google(audio, language='pt'))

        sexta.say('Diga o segundo valor')
        print('Diga o segundo valor')
        sexta.runAndWait()
        print('Mic On')
        reconhecedor.adjust_for_ambient_noise(mic)
        audio = reconhecedor.record(mic, duration=10, offset=None)
        b = float(reconhecedor.recognize_google(audio, language='pt'))

        if operacao == 'DIVISÃO' and b == 0:
            return "Divisão por zero não é permitida."
        
        expressao = f'{a} {operacoes_validas[operacao]} {b}'
        resultado = eval(expressao)
        return resultado
        
def pegarTemperatura():
    with sr.Microphone() as mic:
        sexta.say('Informe uma cidade')
        print('Informe uma cidade')
        sexta.runAndWait()
        print('Mic On')
        reconhecedor.adjust_for_ambient_noise(mic)
        audio = reconhecedor.record(mic, duration=10, offset=None)
        cidade = reconhecedor.recognize_google(audio, language='pt')
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid=ff484b2cba75bb4b8a2a5ea0d63184b9&units=metric')
        data = response.json()
        temperatura = data['main']['temp']
        temperaturaAtual = f"A temperatura da cidade de {cidade} é de {temperatura} graus Celsius."
        print(temperaturaAtual)
        sexta.say(temperaturaAtual)
        sexta.runAndWait()
    except Exception as e:
        print(f"Erro ao obter temperatura: {e}")
        sexta.say("Desculpe, ocorreu um erro ao obter a temperatura.")
        print("Desculpe, ocorreu um erro ao obter a temperatura.")
        sexta.runAndWait()

def recomenda_serie(genero): 
    url = "https://api.themoviedb.org/3/discover/tv"
    params = {
        "api_key": "f15b890b265a85debc3910026ec0c98e",
        "sort_by": "popularity.desc",
        "with_genres": genero,
        "page": 1
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        total_results = data["total_results"]
        if total_results > 0:
            series = data["results"]
            serie_aleatoria = random.choice(series)
            titulo = serie_aleatoria["name"]
            sexta.say(f"Te recomendo a série: {titulo}")
            sexta.runAndWait()
            print(f"Te recomendo a série: {titulo}")
        else:
            sexta.say("Nenhuma série encontrada para o gênero especificado.")
            print("Nenhuma série encontrada para o gênero especificado.")
            sexta.runAndWait()
    else:
        sexta.say("Não foi possível obter as séries aleatórias.")
        print("Não foi possível obter as séries aleatórias.")
        sexta.runAndWait()

def obter_conselho():
    url = "https://api.adviceslip.com/advice?lang=pt"
    response = requests.get(url)
    
    if response.status_code == 200:
        advice_data = response.json()
        conselho = advice_data["slip"]["advice"]
        translator = Translator()
        translated_advice = translator.translate(conselho, src='en', dest='pt').text
        sexta.say(conselho)
        print(conselho)
        sexta.runAndWait()
        
        return conselho
    else:
        return None

def traduzir_texto():
    sexta.say("Qual texto você deseja traduzir?")
    sexta.runAndWait()
    texto = sexta_escuta()
    tradutor = Translator()
    texto_traduzido = tradutor.translate(texto, dest='en')
    sexta.say(f"O texto traduzido para o inglês é {texto_traduzido}")
    print(f"O texto traduzido para o inglês é {texto_traduzido}")
    sexta.runAndWait()

def buscar_endereco(cep):
    endpoint = f'https://viacep.com.br/ws/{cep}/json/'
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        endereco = response.json()

        if 'erro' not in endereco:
            logradouro = endereco['logradouro']
            complemento = endereco['complemento']
            bairro = endereco['bairro']
            localidade = endereco['localidade']
            uf = endereco['uf']
            cep = endereco['cep']

            sexta.say(f"Endereço encontrado para o CEP {cep}:")
            print(f"Endereço encontrado para o CEP {cep}:")
            sexta.runAndWait()
            sexta.say(f"{logradouro}, {complemento}, bairro {bairro} em {localidade}")
            print(f"{logradouro}, {complemento}, bairro {bairro} em {localidade}")
            sexta.runAndWait()
            
        else:
            print(f"Não foi possível encontrar o endereço para o CEP {cep}.")
    except requests.exceptions.RequestException as e:
        print("Ocorreu um erro ao se conectar à API:", e)

# Listas de comandos

cad_evento = ['CADASTRAR EVENTO NA AGENDA', 'CADASTRAR EVENTO', 'TENHO UM EVENTO',
              'REGISTRAR EVENTO NA AGENDA', 'CADASTRO DE EVENTO', 'ADICIONAR NOVO EVENTO', 'COLOCA NA MINHA AGENDA']
ler_agenda = ['LER AGENDA', 'AGENDA', 'COMPROMISSOS', 'MEUS COMPROMISSOS']
horario = ['QUE HORAS SÃO?', 'ME DIGA AS HORAS']

while True:
    if inicia_sexta():
        while True:
            comando = sexta_escuta()
            # Função para cadastrar evento
            if comando in cad_evento or 'EVENTO' in comando:
                cadastrar_evento()
            # Função para ler a agenda
            elif comando in ler_agenda or 'AGENDA' in comando:
                leitura_agenda()
            # Função 1: Baixar e escutar música
            elif 'MÚSICA' in comando:
                baixar_musica()
            # Função 2: Fazer pesquisas web
            elif 'PESQUISA' in comando or 'GOOGLE' in comando:
                pesquisa_web()
            # Função 3: Cotação do dolar
            elif 'COTAÇÃO' in comando:
                obter_cotacao_dolar()
            # Função 4: Calculadora
            elif 'CALCULADORA' in comando or 'CALCULAR' in comando:
                resultado = calculadora()
                sexta.say(resultado)
                sexta.runAndWait()
            # Função 5: Temperatura
            elif 'TEMPERATURA' in comando or 'GRAUS' in comando:
                pegarTemperatura()            
            # Função 6: Informar a hora atual
            elif comando in horario or 'HORAS' in comando:
                hora = datetime.datetime.now().strftime('%H:%M')
                sexta.say('Agora são ' + hora)
                sexta.runAndWait()
            #Função 7: obter recomendação de série
            elif "SÉRIE" in comando:
                with sr.Microphone() as mic:
                    sexta.say('Qual gênero você deseja?')
                    sexta.runAndWait()
                    print('Mic On')
                    reconhecedor.adjust_for_ambient_noise(mic)
                    audio = reconhecedor.record(mic, duration=10, offset=None)
                    genero = reconhecedor.recognize_google(audio, language='pt')
                    recomenda_serie(genero)
                break
            #Função 8: Obter conselho
            elif "CONSELHO" in comando:
                obter_conselho()
            #Função 9: Traduzir texto pro Ingles
            elif "TRADUZIR" in comando:
                traduzir_texto()
            #Função 10: Contar uma piada
            elif "CEP" in comando or "ENDEREÇO" in comando:
                with sr.Microphone() as mic:
                    sexta.say('Qual CEP você deseja pesquisar?')
                    print('Qual CEP você deseja pesquisar?')
                    sexta.runAndWait()
                    print('Mic On')
                    reconhecedor.adjust_for_ambient_noise(mic)
                    audio = reconhecedor.record(mic, duration=10, offset=None)
                    cep = reconhecedor.recognize_google(audio, language='pt')
                    buscar_endereco(cep)
            elif "SAIR" in comando or "ENCERRAR" in comando or "OBRIGADA" in comando:
                sexta.say("Até logo! Encerrando o programa.")
                print("Até logo! Encerrando o programa.")
                sexta.runAndWait()
                exit()
            else:
                print("Comando não entendido.")
                break