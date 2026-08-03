
**AUTOMAÇÃO DE MONITORAMENTO E ALERTAS DE VOOS (FLIGHTRADAR24)**


1. DESCRIÇÃO GERAL
------------------
Este programa em Python realiza a raspagem de dados em tempo real no
Flightradar24 para identificar voos em rota em direção ao aeroporto,
extrai seus dados operacionais, formata um briefing e envia as 
notificações diretamente via WhatsApp.

Quando o voo estiver a 15 minutos do pouso, um alerta de prioridade
é disparado informando a aproximação e pouso iminente.


2. BIBLIOTECAS NECESSÁRIAS
--------------------------
Para o correto funcionamento do script, instale as seguintes dependências.

Crie um arquivo chamado "requirements.txt" e adicione o conteúdo abaixo:

undetected-chromedriver
selenium


Comando para instalação via terminal:
pip install -r requirements.txt


3. FLUXO DE FUNCIONAMENTO DO PROGRAMA
------------------------------------
- Passo 1: O robô utiliza o undetected-chromedriver para abrir a lista
  de chegadas do aeroporto no Flightradar24 sem ser bloqueado.
- Passo 2: Varre a lista filtrando apenas os voos com o status LIVE 
  (que já decolaram e estão em rota).
- Passo 3: Clica em cada voo LIVE para abrir a aba lateral de detalhes 
  e extrai:
    * Número do voo (chegada e saída)
    * Modelo da aeronave
    * Prefixo (matrícula da aeronave)
    * Horário estimado/agendado de chegada
    * Horário real de decolagem
- Passo 4: Calcula a diferença de tempo e formata a mensagem do briefing.
- Passo 5: Encaminha o briefing para o WhatsApp configurado.
- Passo 6: Quando o tempo restante for de 15 minutos ou menos, dispara
  um alerta prioritário informando o pouso iminente do voo.


4. MODELO DA MENSAGEM (BRIEFING)
--------------------------------
🚨 BRIEFFING 🚨

✈️ [Número do Voo] ✈️
✅ Status: DECOLADO
🛬 Chegada: [Horário] 🛬
⏰ Tempo restante: [Tempo]
🛩️ Aeronave: [Modelo]
ℹ️ Prefixo: [Matrícula]
====================================================================
