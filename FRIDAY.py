from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import os
from pytube import YouTube
import youtube_dl as yt

# Função de escutar


def sexta_escuta(eventos_validos=[]):
    while True:
        print('Mic On')
        if eventos_validos == []:
            try:
                reconhecedor.adjust_for_ambient_noise(mic)
                audio = reconhecedor.record(mic, duration=10, offset=None)
                texto = reconhecedor.recognize_google(audio, language='pt')
                return texto.upper()
            except Exception as err:
                print(f'erro ignorado: {err}')
                pass
        else:
            try:
                reconhecedor.adjust_for_ambient_noise(mic)
                audio = reconhecedor.record(mic, duration=10, offset=None)
                texto = reconhecedor.recognize_google(audio, language='pt')
                if texto.upper() in eventos_validos:
                    return True
                else:
                    raise ValueError('Poderia repetir por favor?')
            except Exception as err:
                print(f'erro ignorado: {err}')
                pass


# EVENTOS A RECONHECER
cad_evento = ['CADASTRAR EVENTO NA AGENDA', 'CADASTRAR EVENTO', 'TENHO UM EVENTO',
              'REGISTRAR EVENTO NA AGENDA', 'CADASTRO DE EVENTO', 'ADICIONAR NOVO EVENTO', 'COLOCA NA MINHA AGENDA']
ler_agenda = ['LER AGENDA', 'MEUS COMPROMISSOS']
positivas = ['OK', 'SIM', 'PODE SER', 'QUERO', 'BORA']
play_song = ['TOCA UMA MUSICA']

reconhecedor = sr.Recognizer()
microfone = sr.Microphone()

with sr.Microphone() as mic:
    print('Mic On')
    reconhecedor.adjust_for_ambient_noise(mic)
    audio = reconhecedor.record(mic, duration=10, offset=None)
    texto = reconhecedor.recognize_google(audio, language='pt')
    init = ['OK SEXTA-FEIRA', 'SEXTA-FEIRA']
    if texto.upper() in init:
        audio = gTTS("Como posso ajudá-lo, senhor Stark?", lang='pt')
        audio.save('init.mp3')
        playsound('init.mp3')
        print("Como posso ajuda-lo, senhor Stark?")
    else:
        print('ALERTA! Comando não autorizado. Segurança a caminho.')
        exit()

# CADASTRO DE EVENTO

    def cadastrar_evento():
        audio = gTTS("Qual evento devo cadastrar?", lang='pt')
        audio.save('cadastro.mp3')
        playsound('cadastro.mp3')
        print("Qual evento devo cadastrar?")
        evento = sexta_escuta()
        try:
            with open('agenda.txt', 'a') as cad:
                cad.write("- " + evento + "\n")
            return True
        except Exception as err:
            print(f'Erro encontrado: {err}')
            return False

    if sexta_escuta(cad_evento):
        while True:
            if cadastrar_evento():
                audio = gTTS(
                    "Evento cadastrado com sucesso! Deseja cadastrar mais algum evento?", lang='pt')
                audio.save('cadastradocomsucesso.mp3')
                playsound('cadastradocomsucesso.mp3')
                print(
                    "Evento cadastrado com sucesso! Deseja cadastrar mais algum evento?")
                if sexta_escuta(positivas):
                    audio = gTTS(
                        "Entendi. Qual evento devo cadastrar?", lang='pt')
                    audio.save('novocadastro.mp3')
                    playsound('novocadastro.mp3')
                    print("Entendi. Qual evento devo cadastrar?")
                else:
                    break

# Ler agenda

    if sexta_escuta(ler_agenda):

        audio = gTTS("Certo. Aqui estão seus compromissos: ", lang='pt')
        audio.save('agenda.mp3')
        playsound('agenda.mp3')
        print("Certo. Aqui estão seus compromissos: ")
    with open('agenda.txt', 'r') as agenda:
        lines = agenda.readlines()
        for i, conteudo in enumerate(lines):
            audio_filename = f'agenda_{i}.mp3'
            audio = gTTS(f'{conteudo}', lang='pt')
            audio.save(audio_filename)
            playsound(audio_filename)
            print(conteudo)

# Tocar uma musica


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

# Pesquisar e obter a URL de um vídeo do YouTube pelo nome da música

with microfone as mic:
    reconhecedor.adjust_for_ambient_noise
    print("Qual musica deseja procurar?")
    audio = reconhecedor.listen(mic)
    musica = reconhecedor.recognize_google(audio, language='en')
    print(musica)
song_name = musica
video_url = buscar_video(song_name)

    #BAIXAR A MUSICA
yt = YouTube(str(video_url))
video = yt.streams.filter(only_audio=True).first()
destination = str(("."))
out_file = video.download(output_path=destination)
base, ext = os.path.splitext(out_file)
new_file = base + '.mp3'
os.rename(out_file, new_file)
os.system(f'start "" "{new_file}"')