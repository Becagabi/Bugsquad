# BUGSQUAD

## Sobre o Projeto
BugSquad é uma poderosa ferramenta de stress testing desenvolvida para analisar a performance de aplicações web e realizar diversos tipos de ataques. Criada pela equipe BugSquad durante o Challenge 2024 de Defesa Cibernética da FIAP, ficamos entre os 10 finalistas! 

## Tipos de Ataque Suportados
- **HTTP Flood**

## Funcionalidades
- Análise de performance de aplicações web sob carga intensa.
- Testes de estresse personalizados com diversos tipos de ataques.
- Portabilidade e escalabilidade garantidas com Docker.

## 🛠️ Tecnologias Utilizadas
- **Python**: para execução do script.
- **Docker**: para portabilidade e fácil replicação do ambiente.

## 📜 Código
O código implementa um ataque HTTP Flood, verificando a presença de WAF e contornando desafios do Cloudflare. Principais componentes:

- **Classe `Cloudflare`**: Detecta e tenta contornar desafios do Cloudflare.
- **Classe `WAFBypass`**: Implementa a lógica de contorno do WAF.
- **Classe `Attack`**: Gerencia o alvo e verifica a presença do WAF.
- **Funções Assíncronas**: Executam requisições HTTP de forma contínua, com opções de métodos e headers variados.

Para mais informações, consulte o código completo.
