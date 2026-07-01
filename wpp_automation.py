import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import locale
import chromedriver_autoinstaller

# CONFIGURAÇÕES GLOBAIS
WAIT_SEARCH_BOX = 30
WAIT_CONTATO = 8                      # tempo de espera por CADA candidato na busca
WAIT_BTN_ENVIAR = 10

SLEEP_APOS_DIGITAR_CONTATO = 2
SLEEP_APOS_CLICAR_CONTATO = 3
SLEEP_APOS_CLICAR_ANEXAR = 2
SLEEP_APOS_ENVIAR_PDF = 5
SLEEP_APOS_ENVIAR_MENSAGEM = 5
SLEEP_FINAL = 3

# Candidatos de busca, em ordem de prioridade.
# Ajuste o DDD/país do número conforme necessário caso a formatação
# exibida pelo WhatsApp Web seja diferente da sua região.
NUMERO_BRUTO = "984762085"
NUMERO_FORMATADO = NUMERO_BRUTO[:5] + "-" + NUMERO_BRUTO[5:]   # 98476-2085

CANDIDATOS_CONTATO = [
    "Elielson",
    "Sísifo",
    NUMERO_BRUTO,
    NUMERO_FORMATADO,
]

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
chromedriver_autoinstaller.install()

def encontrar_primeiro_pdf():
    downloads_path = os.path.expanduser("~/Downloads")
    try:
        arquivos = os.listdir(downloads_path)
        for arquivo in arquivos:
            if arquivo.lower().endswith('.pdf'):
                return os.path.join(downloads_path, arquivo)
    except Exception as e:
        print(f"Erro ao acessar pasta Downloads: {e}")
    return None

def localizar_caixa_busca(driver):
    return WebDriverWait(driver, WAIT_SEARCH_BOX).until(
        EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab]"))
    )

def limpar_caixa_busca(search_box):
    search_box.click()
    search_box.send_keys(Keys.CONTROL, "a")
    search_box.send_keys(Keys.BACKSPACE)

def localizar_contato(driver, candidatos):
    """
    Tenta, em ordem, cada nome/número da lista de candidatos na busca do WhatsApp.
    Retorna o elemento clicável do primeiro que for encontrado, ou None se nenhum bater.
    """
    for candidato in candidatos:
        print(f"Procurando por '{candidato}'...")
        try:
            search_box = localizar_caixa_busca(driver)
            limpar_caixa_busca(search_box)
            search_box.send_keys(candidato)
            time.sleep(SLEEP_APOS_DIGITAR_CONTATO)

            elemento = WebDriverWait(driver, WAIT_CONTATO).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//span[@title='{candidato}' or contains(@title, '{candidato}')]")
                )
            )
            print(f"Contato encontrado com o termo '{candidato}'.")
            return elemento
        except TimeoutException:
            print(f"Nada encontrado para '{candidato}'.")
            continue

    return None

def criar_driver():
    # Perfil dedicado à automação, fora da pasta padrão do Chrome. Desde o
    # Chrome 136+, apontar o --user-data-dir para o diretório padrão do
    # Chrome ("...\Google\Chrome\User Data") bloqueia a porta de remote
    # debugging por segurança, causando "DevToolsActivePort file doesn't
    # exist". Um perfil próprio evita esse bloqueio.
    user_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chrome_profile")

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    return webdriver.Chrome(options=options)

def abrir_whatsapp_web(driver):
    print("Abrindo WhatsApp Web...")
    driver.get("https://web.whatsapp.com")
    input("Escaneie o QR Code no WhatsApp Web (se necessário) e pressione Enter...")

def anexar_pdf(driver, caminho_pdf):
    print("Anexando arquivo...")
    btn_anexar = driver.find_element(By.XPATH, "//div[@title='Anexar']")
    btn_anexar.click()
    time.sleep(SLEEP_APOS_CLICAR_ANEXAR)

    try:
        btn_documento = driver.find_element(By.XPATH, "//input[@accept='*' and @type='file']")
        btn_documento.send_keys(caminho_pdf)
        time.sleep(SLEEP_APOS_ENVIAR_PDF)
    except Exception as e:
        print(f"Seletor padrão de anexo falhou ({e}), tentando caminho alternativo...")
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

def enviar_pdf_whatsapp():
    caminho_pdf = encontrar_primeiro_pdf()
    if not caminho_pdf:
        print("Nenhum arquivo PDF encontrado na pasta Downloads!")
        return
    print(f"Arquivo encontrado: {caminho_pdf}")

    try:
        driver = criar_driver()
    except Exception as e:
        print(f"Falha ao iniciar o Chrome: {e}")
        print("Tente fechar manualmente qualquer instância do Chrome e executar novamente.")
        return

    try:
        abrir_whatsapp_web(driver)

        contato = localizar_contato(driver, CANDIDATOS_CONTATO)
        if contato is None:
            print("Nenhum dos contatos/números configurados foi encontrado!")
            return

        contato.click()
        time.sleep(SLEEP_APOS_CLICAR_CONTATO)

        anexar_pdf(driver, caminho_pdf)

    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        time.sleep(SLEEP_FINAL)
        driver.quit()


if __name__ == "__main__":
    enviar_pdf_whatsapp()