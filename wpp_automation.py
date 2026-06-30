import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


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
    # Encontra o PDF
    caminho_pdf = encontrar_primeiro_pdf()

    if not caminho_pdf:
        print("Nenhum arquivo PDF encontrado na pasta Downloads!")
        return

    print(f"Arquivo encontrado: {caminho_pdf}")

    # Configuração do Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Ajuste para manter o perfil do WhatsApp
    options.add_argument(r"--user-data-dir=C:\Users\SeuUsuario\AppData\Local\Google\Chrome\User Data")

    # Inicializa o driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Abrir WhatsApp Web
        print("Abrindo WhatsApp Web...")
        driver.get("https://web.whatsapp.com")

        # Aguarda o QR Code ser escaneado
        input("Escaneie o QR Code no WhatsApp Web e pressione Enter...")

        # Pesquisar pelo contato "Elielson"
        print("Procurando pelo contato Elielson...")
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        search_box.click()
        search_box.send_keys("Elielson")
        time.sleep(3)

        # Seleciona o contato
        try:
            contato = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@title='Elielson']"))
            )
            contato.click()
            time.sleep(3)
        except:
            print("Contato 'Elielson' não encontrado!")
            return

        # Clica no botão de anexar
        print("Anexando arquivo...")
        btn_anexar = driver.find_element(By.XPATH, "//div[@title='Anexar']")
        btn_anexar.click()
        time.sleep(2)

        # Clica na opção de documento/arquivo
        try:
            btn_documento = driver.find_element(By.XPATH, "//input[@accept='*' and @type='file']")
            btn_documento.send_keys(caminho_pdf)
            time.sleep(5)
        except:
            # Alternativa: clicar no ícone de documento
            btn_doc = driver.find_element(By.XPATH, "//div[@title='Documento']")
            btn_doc.click()
            time.sleep(2)

            # Upload do arquivo
            input_file = driver.find_element(By.XPATH, "//input[@type='file']")
            input_file.send_keys(caminho_pdf)
            time.sleep(5)

        # Envia o arquivo
        print("Enviando arquivo...")
        btn_enviar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
        )
        btn_enviar.click()

        print("Arquivo enviado com sucesso!")
        time.sleep(5)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    enviar_pdf_whatsapp()
