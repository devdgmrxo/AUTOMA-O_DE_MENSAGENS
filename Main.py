import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from datetime import datetime

options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--user-agent=Mozila/0.5 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36')
navegador = uc.Chrome(options=options, version_main=150)
url = "https://www.flightradar24.com/airport/fln/arrivals"

navegador.get(url)

time.sleep(8)



try:

    fechar_termos = navegador.find_element(By.XPATH, '//*[contains(text(), "Agree and close")]')
    fechar_termos.click()
except Exception:
    pass

time.sleep(5)

try:

    fechar_whats_new = navegador.find_element(By.XPATH, '//button[.//span[contains(text(), "Close")]]')
    fechar_whats_new.click()

except Exception:
    pass

time.sleep(5)

voos_live = navegador.find_elements(By.XPATH, '//li[..//*[local-name()="svg" and contains(@data-name, "LIVE")]]')

for voo in voos_live:
    try:
        try:
            numero_voo = voo.find_element(By.XPATH, './/span[contains(@class, "text-sm") and contains(@class, "truncate")]').text.strip()
        except Exception:
            numero_voo = "N/A"
        voo.click()
        
        time.sleep(5)

        try:
            aeronave = navegador.find_element(By.XPATH, '//dt[text()="Equipment"]/following-sibling::dd//span[contains(@class, "mr-1")]').text.strip()
        except Exception:
            aeronave = "N/A"

        time.sleep(2)
        try:
            prefixo_elem = navegador.find_element(By.XPATH, '//*[@data-testid="airport-flight-details__registration"]')
            prefixo = prefixo_elem.text.replace("\n", "").strip()
        except Exception:
            prefixo = "N/A"

        # Captura da Decolagem Real (Actual departure)
        try:
            decolagem_elem = navegador.find_element(By.XPATH, '//*[@data-testid="airport-flight-details__actual-departure"]')
            horario_decolagem = decolagem_elem.text.replace("\n", " ").strip()
        except Exception:
            horario_decolagem = "N/A"

        # Captura da Chegada Agendada (Scheduled arrival)
        try:
            chegada_elem = navegador.find_element(By.XPATH, '//dt[text()="Scheduled arrival"]/following-sibling::dd')
            horario_chegada = chegada_elem.text.replace("\n", " ").strip()
        except Exception:
            horario_chegada = "N/A"

        # Cálculo da diferença (Chegada Agendada - Decolagem Real)
        tempo_restante = "N/A"
        if horario_decolagem != "N/A" and horario_chegada != "N/A":
            try:
                data_base = datetime.today()
                dt_decolagem = datetime.strptime(horario_decolagem, "%I:%M %p").replace(
                    year=data_base.year, month=data_base.month, day=data_base.day
                )
                dt_chegada = datetime.strptime(horario_chegada, "%I:%M %p").replace(
                    year=data_base.year, month=data_base.month, day=data_base.day
                )
                
                diferenca = dt_chegada - dt_decolagem
                minutos_totais = int(diferenca.total_seconds() // 60)

                if minutos_totais > 0:
                    horas = minutos_totais // 60
                    minutos = minutos_totais % 60
                    tempo_restante = f"{horas}h{minutos:02d}min" if horas > 0 else f"{minutos}min"
            except Exception:

                tempo_restante = "N/A"

        briefing = f"""
🚨 BRIEFFING 🚨

✈️ {numero_voo} ✈️
✅ Status: DECOLADO
🛬 Chegada: {horario_chegada} 🛬
⏰ Tempo restante: {tempo_restante}
🛩️ Aeronave: {aeronave}
ℹ️ Prefixo: {prefixo}"""

        print(briefing)
        print("\n" + "=" * 40 + "\n")
    except Exception as e:
        print(f"Erro ao capturar dados do voo: {e}")

input("Pressione ENTER no terminal para fechar...") 
