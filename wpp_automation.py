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
WAIT_SEARCH_BOX = 10
WAIT_CONTATO = 20                      # tempo de espera por CADA candidato na busca
WAIT_BTN_ENVIAR = 10

SLEEP_APOS_DIGITAR_CONTATO = 2
SLEEP_APOS_CLICAR_CONTATO = 3
SLEEP_APOS_CLICAR_ANEXAR = 2
SLEEP_APOS_ENVIAR_PDF = 5
SLEEP_APOS_ENVIAR_MENSAGEM = 5
SLEEP_FINAL = 3

# Candidato de busca. Ajuste conforme necessário caso a formatação
# exibida pelo WhatsApp Web seja diferente da sua região.
NUMERO_FORMATADO = "8476-2085"

CANDIDATOS_CONTATO = [
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
        EC.presence_of_element_located(
            (By.XPATH, "//div[@data-testid='chat-list-search-container']//input[@type='text']")
        )
    )

def limpar_caixa_busca(search_box):
    search_box.click()
    search_box.send_keys(Keys.CONTROL, "a")
    search_box.send_keys(Keys.BACKSPACE)

def localizar_contato(driver, candidatos):
    """
    Tenta, em ordem, cada nome/número da lista de candidatos na busca do WhatsApp.
    Retorna o elemento clicável do primeiro resultado da lista de busca, ou None
    se nenhum candidato retornar resultado.
    """
    for candidato in candidatos:
        print(f"Procurando por '{candidato}'...")
        try:
            search_box = localizar_caixa_busca(driver)
            limpar_caixa_busca(search_box)
            search_box.send_keys(candidato)
            time.sleep(SLEEP_APOS_DIGITAR_CONTATO)

            # A primeira "row" da lista de resultados pode ser um cabeçalho de
            # seção (ex: "Conversas"), que não é clicável e não tem gridcell.
            # Por isso buscamos direto pelo primeiro gridcell clicável
            # (tabindex="0"), que é o real item de contato/conversa.
            elemento = WebDriverWait(driver, WAIT_CONTATO).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "(//div[@id='pane-side']//div[@role='gridcell'][@tabindex='0'])[1]")
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

def abrir_conversa(driver, contato):
    contato.click()
    time.sleep(SLEEP_APOS_CLICAR_CONTATO)
    # Confirma que a conversa realmente abriu, esperando a caixa de digitar
    # mensagem aparecer. Se o clique não tiver aberto nada, isso levanta
    # TimeoutException em vez de seguir silenciosamente para o próximo passo.
    WebDriverWait(driver, WAIT_CONTATO).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@data-testid='conversation-compose-box-input']")
        )
    )

def _tornar_interagivel(driver, elemento):
    # O input de arquivo do "Documento" fica com display:none, e essa versão
    # do ChromeDriver recusa send_keys em elemento de tamanho zero
    # ("element not interactable: element has zero size"). Forçar visibilidade
    # via JS não abre nenhum diálogo real, só libera a interação do Selenium.
    driver.execute_script(
        "arguments[0].style.display='block'; arguments[0].style.visibility='visible'; "
        "arguments[0].style.opacity='1'; arguments[0].style.height='1px'; arguments[0].style.width='1px';",
        elemento,
    )

def anexar_pdf(driver, caminho_pdf):
    print("Anexando arquivo...")
    btn_anexar = WebDriverWait(driver, WAIT_BTN_ENVIAR).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Anexar']"))
    )
    btn_anexar.click()
    time.sleep(SLEEP_APOS_CLICAR_ANEXAR)

    btn_documento = WebDriverWait(driver, WAIT_BTN_ENVIAR).until(
        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Documento']"))
    )
    btn_documento.click()
    time.sleep(SLEEP_APOS_CLICAR_ANEXAR)

    input_file = driver.find_element(By.XPATH, "//input[@type='file' and not(contains(@accept, 'image'))]")
    _tornar_interagivel(driver, input_file)
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

        abrir_conversa(driver, contato)

        anexar_pdf(driver, caminho_pdf)

    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        time.sleep(SLEEP_FINAL)
        driver.quit()


if __name__ == "__main__":
    enviar_pdf_whatsapp()