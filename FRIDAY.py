from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
import os

reconhecedor = sr.Recognizer()
microfone = sr.Microphone()

with sr.Microphone() as mic:
    reconhecedor.adjust_for_ambient_noise(mic)
    audio = reconhecedor.record(mic, duration=10, offset=None)
    texto = reconhecedor.recognize_google(audio, language='pt')
    init = ['OK SEXTA-FEIRA', 'SEXTA-FEIRA', 'OLA SEXTA-FEIRA']
    if texto.upper() in init:
        audio = gTTS("Como posso ajudá-lo, senhor Stark?", lang='pt')
        audio.save('init.mp3')
        playsound('init.mp3')
        print("Como posso ajuda-lo, senhor Stark?")
    else:
        print('Comando não autorizado. Segurança a caminho.')
        exit()
   #cadastrar evento
    continuar = True
    while continuar:
        reconhecedor.adjust_for_ambient_noise(mic)
        audio = reconhecedor.record(mic, duration=5, offset=None)
        texto = reconhecedor.recognize_google(audio, language='pt')
        cadastrar_evento = ['CADASTRAR EVENTO NA AGENDA', 'TENHO UM EVENTO', 'REGISTRAR EVENTO NA AGENDA']
        if texto.upper() in cadastrar_evento:
            audio = gTTS("Ok, qual evento devo cadastrar?", lang='pt')
            audio.save('cadastro.mp3')
            playsound('cadastro.mp3')
            print("Ok, qual evento devo cadastrar?")
            
            reconhecedor.adjust_for_ambient_noise(mic)
            audio = reconhecedor.record(mic, duration=5, offset=None)
            evento = reconhecedor.recognize_google(audio, language='pt')
            
            with open('agenda.txt', 'a') as cad:
                cad.write(evento + "\n")
            
            audio = gTTS("Evento cadastrado com sucesso! Deseja cadastrar mais algum evento?", lang='pt')
            audio.save('cadastradocomsucesso.mp3')
            playsound('cadastradocomsucesso.mp3')
            print("Evento cadastrado com sucesso! Deseja cadastrar mais algum evento?")

#FUNCIONA ATÉ AQUI
            
            reconhecedor.adjust_for_ambient_noise(mic)
            audio = reconhecedor.record(mic, duration=5, offset=None)
            resposta = reconhecedor.recognize_google(audio, language='pt')
            positivas = ['OK', 'SIM', 'PODE SER', 'QUERO', 'BORA']
            
            if resposta.upper() not in positivas:
                continuar = False
#Ler agenda
    
    reconhecedor.adjust_for_ambient_noise(mic)
    audio = reconhecedor.record(mic, duration=10, offset=None)
    texto = reconhecedor.recognize_google(audio, language='pt')
    ler_agenda = ['LER MINHA AGENDA', 'O QUE TENHO HOJE?', 'QUAIS SÃO MEUS COMPROMISSOS?']
    if texto.upper() in ler_agenda:
        with open('agenda.txt', 'r') as agenda:
            conteudo = agenda.read()
            print(conteudo)  
            audio = gTTS("Certo. Aqui estão seus compromissos: ", conteudo, lang='pt')
            audio.save('agenda.mp3')
            playsound('agenda.mp3')
            print("Certo. Aqui estão seus compromissos: ", conteudo)