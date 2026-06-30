import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# ============================================================
# CONFIGURAÇÕES GLOBAIS - Tempos de espera (em segundos)
# ============================================================

# --- Perfil do Chrome ---
PERFIL_CHROME = "Profile 2"  # Altere para o perfil desejado ("Default", "Profile 1", etc.)

# --- Tempos de espera para elementos da página ---
WAIT_SEARCH_BOX = 30  # Tempo máximo para a caixa de pesquisa do WhatsApp aparecer
WAIT_CONTATO = 10  # Tempo máximo para encontrar o contato
WAIT_BTN_ENVIAR = 10  # Tempo máximo para o botão de enviar ficar clicável

# --- Pausas fixas entre ações (sleeps) ---
SLEEP_APOS_DIGITAR_CONTATO = 3  # Aguarda após digitar o nome do contato
SLEEP_APOS_CLICAR_CONTATO = 3  # Aguarda após clicar no contato
SLEEP_APOS_CLICAR_ANEXAR = 2  # Aguarda após clicar no botão anexar
SLEEP_APOS_ENVIAR_PDF = 5  # Aguarda após enviar o caminho do PDF (upload)
SLEEP_APOS_ENVIAR_MENSAGEM = 5  # Aguarda após clicar no botão enviar
SLEEP_FINAL = 3  # Pausa antes de fechar o navegador


# ============================================================

def obter_nome_perfil_por_indice(indice):
    """Retorna o nome do perfil baseado no índice: 0->Default, 1->Profile 1, ..."""
    if indice == 0:
        return "Default"
    else:
        return f"Profile {indice}"


# (Opcional) Se preferir usar índice, descomente a linha abaixo:
# PERFIL_CHROME = obter_nome_perfil_por_indice(1)

def encontrar_primeiro_pdf():
    """Encontra o primeiro arquivo PDF na pasta Downloads"""
    downloads_path = os.path.expanduser("~/Downloads")
    try:
        arquivos = os.listdir(downloads_path)
        for arquivo in arquivos:
            if arquivo.lower().endswith('.pdf'):
                return os.path.join(downloads_path, arquivo)
    except Exception as e:
        print(f"Erro ao acessar pasta Downloads: {e}")
    return None

def enviar_pdf_whatsapp():
    caminho_pdf = encontrar_primeiro_pdf()
    if not caminho_pdf:
        print("Nenhum arquivo PDF encontrado na pasta Downloads!")
        return
    print(f"Arquivo encontrado: {caminho_pdf}")

    # Configuração do Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    user_data_dir = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data"
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={PERFIL_CHROME}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("Abrindo WhatsApp Web...")
        driver.get("https://web.whatsapp.com")
        input("Escaneie o QR Code no WhatsApp Web e pressione Enter...")

        print("Procurando pelo contato Elielson...")
        search_box = WebDriverWait(driver, WAIT_SEARCH_BOX).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        search_box.click()
        search_box.send_keys("Elielson")
        time.sleep(SLEEP_APOS_DIGITAR_CONTATO)

        try:
            contato = WebDriverWait(driver, WAIT_CONTATO).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@title='Elielson']"))
            )
            contato.click()
            time.sleep(SLEEP_APOS_CLICAR_CONTATO)
        except:
            print("Contato 'Elielson' não encontrado!")
            return

        print("Anexando arquivo...")
        btn_anexar = driver.find_element(By.XPATH, "//div[@title='Anexar']")
        btn_anexar.click()
        time.sleep(SLEEP_APOS_CLICAR_ANEXAR)

        try:
            btn_documento = driver.find_element(By.XPATH, "//input[@accept='*' and @type='file']")
            btn_documento.send_keys(caminho_pdf)
            time.sleep(SLEEP_APOS_ENVIAR_PDF)
        except:
            btn_doc = driver.find_element(By.XPATH, "//div[@title='Documento']")
            btn_doc.click()
            time.sleep(SLEEP_APOS_CLICAR_ANEXAR)
            input_file = driver.find_element(By.XPATH, "//input[@type='file']")
            input_file.send_keys(caminho_pdf)
            time.sleep(SLEEP_APOS_ENVIAR_PDF)

        print("Enviando arquivo...")
        btn_enviar = WebDriverWait(driver, WAIT_BTN_ENVIAR).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
        )
        btn_enviar.click()
        print("Arquivo enviado com sucesso!")
        time.sleep(SLEEP_APOS_ENVIAR_MENSAGEM)

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        time.sleep(SLEEP_FINAL)
        driver.quit()

if __name__ == "__main__":
    enviar_pdf_whatsapp()