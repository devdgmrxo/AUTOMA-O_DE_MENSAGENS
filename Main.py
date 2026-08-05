import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re
import requests

def criar_navegador():
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-first-run')
    options.add_argument('--no-service-autorun')
    options.add_argument('--password-store=basic')
    
    return uc.Chrome(options=options, version_main=150, use_subprocess=True)

navegador = criar_navegador()



url = "https://www.flightradar24.com/airport/fln/arrivals"

print('=' * 30)
print(f'{"PROGRAMA INICIADO":^30}')
print('=' * 30)

try:
    navegador.get(url)
    time.sleep(8)

    try:
        fechar_termos = navegador.find_element(By.XPATH, '//*[contains(text(), "Agree and close")]')
        fechar_termos.click()
    except Exception:
        pass

    time.sleep(3)

    try:
        fechar_whats_new = navegador.find_element(By.XPATH, '//button[.//span[contains(text(), "Close")]]')
        fechar_whats_new.click()
    except Exception:
        pass

    time.sleep(3)

    janela_principal = navegador.current_window_handle

    voos_live = navegador.find_elements(By.XPATH, '//li[..//*[local-name()="svg" and contains(@data-name, "LIVE")]]')

    for voo in voos_live:
        try:
            # 1. Numero do Voo da lista
            try:
                numero_voo = voo.find_element(By.XPATH, './/span[contains(@class, "text-sm") and contains(@class, "truncate")]').text.strip()
            except Exception:
                numero_voo = "N/A"

            # 2. Clica para abrir o painel lateral no mesmo formato do seu original
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", voo)
            time.sleep(1)
            voo.click()
            time.sleep(4)

            # 3. Extrai os dados do painel lateral (seu seletor original)
            try:
                aeronave = navegador.find_element(By.XPATH, '//dt[text()="Equipment"]/following-sibling::dd//span[contains(@class, "mr-1")]').text.strip()
            except Exception:
                aeronave = "N/A"

            try:
                prefixo_elem = navegador.find_element(By.XPATH, '//*[@data-testid="airport-flight-details__registration"]')
                prefixo = prefixo_elem.text.replace("\n", "").strip()
            except Exception:
                prefixo = "N/A"

            try:
                call_sign = navegador.find_element(By.XPATH, '//div[@testid="airport-flight-details__callsign"]').text.strip()
            except Exception:
                call_sign = "N/A"

            # 4. Captura o link real do voo gerado no painel lateral
            link_voo = None
            try:
                link_elem = navegador.find_element(By.XPATH, '//a[contains(@href, "/flight/")] | //a[contains(@href, "/data/flights/")]')
                link_voo = link_elem.get_attribute("href")
            except Exception:
                if call_sign != "N/A" and call_sign != "":
                    link_voo = f"https://www.flightradar24.com/{call_sign}"

            tempo_formatado = "N/A"

            # 5. Nova aba para pegar o tempo restante (VERSÃO CORRIGIDA)
            if link_voo:
                try:
                    navegador.switch_to.new_window('tab')
                    navegador.get(link_voo)

                    wait = WebDriverWait(navegador, 10)
                    
                    # PRIMEIRO: verifica se o voo JÁ CHEGOU
                    try:
                        status_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Arrived") or contains(text(), "Landed")]'))
                        )
                        tempo_formatado = "JÁ CHEGOU"
                    except TimeoutException:
                        # Se NÃO chegou, procura especificamente o elemento com "in"
                        try:
                            # Espera a página carregar os dados
                            time.sleep(2)
                            
                            # Procura TODOS os spans que contém "in" (tempo restante)
                            elementos_tempo = navegador.find_elements(By.XPATH, '//span[contains(text(), "in")]')
                            
                            # Pega o PRIMEIRO que tem "in" (é o tempo restante)
                            for elem in elementos_tempo:
                                texto_bruto = elem.text.strip()
                                # Procura padrão "in 06:47"
                                match = re.search(r'in\s+(\d{1,2}):(\d{2})', texto_bruto)
                                if match:
                                    horas, minutos = match.groups()
                                    tempo_formatado = f"{int(horas):02d}h{minutos}min"
                                    break
                                # Procura padrão "in 6h47min" (formato alternativo)
                                match2 = re.search(r'in\s+(\d{1,2})h(\d{1,2})min', texto_bruto)
                                if match2:
                                    horas, minutos = match2.groups()
                                    tempo_formatado = f"{int(horas):02d}h{minutos}min"
                                    break
                            
                            # Se não achou "in", tenta o seletor antigo como fallback
                            if tempo_formatado == "N/A":
                                try:
                                    elemento_tempo = wait.until(
                                        EC.presence_of_element_located((By.XPATH, '//span[@data-testid="aircraft-small-panel__flight-time-remaining"]'))
                                    )
                                    texto_bruto = navegador.execute_script("return arguments[0].textContent;", elemento_tempo).strip()
                                    match = re.search(r'(\d{1,2}):(\d{2})', texto_bruto)
                                    if match:
                                        horas, minutos = match.groups()
                                        tempo_formatado = f"{int(horas):02d}h{minutos}min"
                                except:
                                    pass
                                    
                        except Exception as e:
                            print(f"Erro ao buscar tempo: {e}")
                            tempo_formatado = "N/A"

                    navegador.close()
                except Exception as e:
                    print(f"Erro ao buscar tempo: {e}")
                    tempo_formatado = "N/A"
                    try:
                        navegador.close()
                    except Exception:
                        pass
                finally:
                    navegador.switch_to.window(janela_principal)

            briefing = f"""
🚨 BRIEFFING 🚨

✈️ {numero_voo} ✈️
✅ Status: DECOLADO
🛬 Chegada:  🛬
⏰ Tempo restante: {tempo_formatado}
🛩️ Aeronave: {aeronave}
ℹ️ Prefixo: {prefixo}
🆔 CallSign: {call_sign}"""

            print(briefing)
            print("\n" + "=" * 30 + "\n")

        except Exception as e:
            print(f"Erro ao capturar dados do voo: {e}")
            navegador.switch_to.window(janela_principal)

finally:
    input("Pressione ENTER no terminal para fechar...")
    try:
        navegador.quit()
    except Exception:
        pass
