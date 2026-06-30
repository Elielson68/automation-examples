import os
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


DRIVER_WAIT_BUTTON_TIME = 1
DRIVER_WAIT_IFRAME_BUTTON_TIME = 1
DRIVER_WAIT_IFRAME_TIME = 1
music_name = "Gorillaz Clint Eastwood"


def baixar_musica():
    # Configuração do Chrome para evitar detecção
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Inicializa o driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Remove a flag de automação do JavaScript
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # PASSO 1: Abrir YouTube diretamente
        print("Abrindo YouTube...")
        driver.get("https://www.youtube.com")
        time.sleep(1)

        # Aceitar cookies se aparecer
        try:
            btn_aceitar = WebDriverWait(driver, DRIVER_WAIT_BUTTON_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Aceitar')]"))
            )
            btn_aceitar.click()
            time.sleep(1)
        except:
            pass

        # PASSO 2: Pesquisar pela música
        print(f"Pesquisando '{music_name}'...")

        #input("espera")

        search_box = WebDriverWait(driver, DRIVER_WAIT_BUTTON_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='search_query']"))
        )
        search_box.clear()
        search_box.send_keys(f"{music_name}")
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)

        # PASSO 3: Clicar no primeiro vídeo
        print("Abrindo o primeiro vídeo...")
        try:
            # Tenta encontrar o primeiro vídeo da lista
            primeiro_video = WebDriverWait(driver, DRIVER_WAIT_BUTTON_TIME).until(
                EC.element_to_be_clickable((By.ID, "video-title"))
            )
            primeiro_video.click()
            time.sleep(1)
        except:
            # Alternativa: usar um seletor mais específico
            primeiro_video = WebDriverWait(driver, DRIVER_WAIT_BUTTON_TIME).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "ytd-video-renderer a#video-title"))
            )
            primeiro_video.click()
            time.sleep(1)

        # Capturar a URL do vídeo
        url_video = driver.current_url
        print(f"URL do vídeo: {url_video}")

        # PASSO 4: Abrir y2meta.is em nova aba
        print("Abrindo y2meta.is...")
        driver.execute_script("window.open('');")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://y2meta.is/pt92/")
        time.sleep(1)

        # PASSO 5: Colar o link do vídeo
        print("Inserindo link para download...")

        # Encontrar o campo de input
        try:
            input_url = WebDriverWait(driver, DRIVER_WAIT_BUTTON_TIME).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Pesquise ou cole o link do youtube aqui...']"))
            )
            input_url.clear()
            input_url.send_keys(url_video)
            print("Aguardando botão de Download ficar pronto...")
            time.sleep(1)

            # ====================================================
            # PARTE MODIFICADA: Resolver o problema do "Loading..." no iframe
            # ====================================================
            try:
                print("Aguardando o carregamento dos botões de download...")

                # Primeiro, encontrar o iframe
                iframe = WebDriverWait(driver, DRIVER_WAIT_IFRAME_TIME).until(
                    EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'dlsrv.online')]"))
                )
                print("Iframe encontrado!")

                # Mudar para o iframe
                driver.switch_to.frame(iframe)
                print("Mudou para o iframe")

                # Agora procurar o botão "Loading..." dentro do iframe
                try:
                    loading_element = WebDriverWait(driver, DRIVER_WAIT_IFRAME_BUTTON_TIME).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//button[contains(@class, 'bg-[#5cb85c]') and @disabled]"))
                    )
                    print("Botão 'Loading...' encontrado dentro do iframe!")

                    # Obtém a posição do elemento
                    location = loading_element.location
                    size = loading_element.size

                    # Calcula o centro do elemento
                    center_x = location['x'] + size['width'] // 2
                    center_y = location['y'] + size['height'] // 2

                    print(f"Posição do Loading: X={center_x}, Y={center_y}")

                    # Move o mouse para o centro do elemento "Loading..."
                    pyautogui.moveTo(center_x, center_y, duration=0.3)
                    print("Mouse posicionado sobre 'Loading...'")

                    # Aguarda 10 segundos com o mouse parado
                    print("Aguardando 10 segundos para os botões aparecerem...")
                    for i in range(3, 0, -1):
                        print(f"{i}...", end=" ", flush=True)
                        time.sleep(0.7)
                    print("\nTempo aguardado!")

                except Exception as e:
                    print(f"Erro ao encontrar o botão dentro do iframe: {e}")

                # Sair do iframe para voltar ao contexto principal
                driver.switch_to.default_content()
                print("Saiu do iframe")

            except Exception as e:
                print(f"Iframe não encontrado. Continuando...")
                print(f"Erro: {e}")
                return

        except Exception as e:
            print(f"deu erro geral")
            return

        # PASSO 6: Selecionar formato MP3 (AGORA DENTRO DO IFRAME)
        print("Selecionando formato MP3...")
        try:
            # Primeiro, entrar no iframe novamente
            iframe = WebDriverWait(driver, DRIVER_WAIT_IFRAME_TIME).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'dlsrv.online')]"))
            )
            driver.switch_to.frame(iframe)
            print("Entrou no iframe para clicar no MP3")

            # Esperar a página de opções carregar
            time.sleep(1)

            # Procurar botão de download MP3
            btn_mp4 = WebDriverWait(driver, DRIVER_WAIT_IFRAME_BUTTON_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-[#5cb85c]')]"))
            )
            btn_mp4.click()

            time.sleep(1)

            if len(driver.window_handles) > 2:
                driver.switch_to.window(driver.window_handles[1])

            time.sleep(1)

            iframe = WebDriverWait(driver, DRIVER_WAIT_IFRAME_TIME).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'dlsrv.online')]"))
            )
            driver.switch_to.frame(iframe)

            # Procurar botão de download MP3
            btn_mp4 = WebDriverWait(driver, DRIVER_WAIT_IFRAME_BUTTON_TIME).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-green-600')]"))
            )
            btn_mp4.click()

            print("Download MP3 iniciado!")
            time.sleep(10)

            # Sair do iframe
            driver.switch_to.default_content()

        except Exception as e:
            print(f"Erro ao tentar baixar o mp3...")
            return

        # PASSO 7: Verificar o download
        print("\nVerificando download...")
        downloads_path = os.path.expanduser("~/Downloads")
        time.sleep(1)

        try:
            arquivos = os.listdir(downloads_path)
            arquivos_ordenados = sorted([f for f in arquivos if os.path.isfile(os.path.join(downloads_path, f))],
                                        key=lambda x: os.path.getmtime(os.path.join(downloads_path, x)),
                                        reverse=True)

            if arquivos_ordenados:
                print(f"Último arquivo baixado: {arquivos_ordenados[0]}")
                print(f"Caminho: {os.path.join(downloads_path, arquivos_ordenados[0])}")
        except Exception as e:
            print(f"Erro ao verificar Downloads: {e}")

        print("\nProcesso concluído! O navegador permanecerá aberto por 5 segundos.")
        time.sleep(5)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        print("\nDica: O site y2meta pode ter mudado sua interface.")
        print("Tente acessar manualmente: https://y2meta.is/pt")
        return

    finally:
        print("\nFechando navegador...")
        driver.quit()


if __name__ == "__main__":

    music = input("Digite o nome da música (deixe vazio para Clint Eastwood): ")
    if music is not None and music != "":
        music_name = music

    baixar_musica()