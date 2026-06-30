import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# ==========================================
# CONFIGURAÇÃO GLOBAL DO PERFIL
# ==========================================
# Defina o nome do perfil desejado (ex: "Default", "Profile 1", "Profile 2")
# Caso queira usar índice, veja a função obter_nome_perfil_por_indice()
PERFIL_CHROME = "Profile 2"  # Altere aqui para o perfil desejado


# ==========================================

def obter_nome_perfil_por_indice(indice):
    """
    Retorna o nome do perfil baseado no índice:
    0 -> "Default"
    1 -> "Profile 1"
    2 -> "Profile 2"
    ...
    """
    if indice == 0:
        return "Default"
    else:
        return f"Profile {indice}"


# Se preferir usar índice, descomente a linha abaixo e comente a variável PERFIL_CHROME
# PERFIL_CHROME = obter_nome_perfil_por_indice(1)  # Altere o número para o perfil desejado

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

    # Caminho base do perfil do Chrome
    user_data_dir = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data"
    options.add_argument(f"--user-data-dir={user_data_dir}")

    # Define o perfil específico usando a variável global
    options.add_argument(f"--profile-directory={PERFIL_CHROME}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("Abrindo WhatsApp Web...")
        driver.get("https://web.whatsapp.com")
        input("Escaneie o QR Code no WhatsApp Web e pressione Enter...")

        print("Procurando pelo contato Elielson...")
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        search_box.click()
        search_box.send_keys("Elielson")
        time.sleep(3)

        try:
            contato = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@title='Elielson']"))
            )
            contato.click()
            time.sleep(3)
        except:
            print("Contato 'Elielson' não encontrado!")
            return

        print("Anexando arquivo...")
        btn_anexar = driver.find_element(By.XPATH, "//div[@title='Anexar']")
        btn_anexar.click()
        time.sleep(2)

        try:
            btn_documento = driver.find_element(By.XPATH, "//input[@accept='*' and @type='file']")
            btn_documento.send_keys(caminho_pdf)
            time.sleep(5)
        except:
            btn_doc = driver.find_element(By.XPATH, "//div[@title='Documento']")
            btn_doc.click()
            time.sleep(2)
            input_file = driver.find_element(By.XPATH, "//input[@type='file']")
            input_file.send_keys(caminho_pdf)
            time.sleep(5)

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