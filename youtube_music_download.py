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
        time.sleep(2)

        # Aceitar cookies se aparecer
        try:
            btn_aceitar = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Aceitar')]"))
            )
            btn_aceitar.click()
            time.sleep(2)
        except:
            pass

        # PASSO 2: Pesquisar pela música
        print("Pesquisando 'Gorillaz Clint Eastwood'...")

        #input("espera")

        search_box = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='search_query']"))
        )
        search_box.clear()
        search_box.send_keys("Gorillaz Clint Eastwood")
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)

        # PASSO 3: Clicar no primeiro vídeo
        print("Abrindo o primeiro vídeo...")
        try:
            # Tenta encontrar o primeiro vídeo da lista
            primeiro_video = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, "video-title"))
            )
            primeiro_video.click()
            time.sleep(1)
        except:
            # Alternativa: usar um seletor mais específico
            primeiro_video = WebDriverWait(driver, 3).until(
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
            input_url = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Pesquise ou cole o link do youtube aqui...']"))
            )
            input_url.clear()
            input_url.send_keys(url_video)
            print("Aguardando botão de Download ficar pronto...")
            time.sleep(3)

            try:
                # Clicar no botão de download
                btn_loading = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Loading...')]"))
                )
                btn_loading.click()
            except:
                print("Deu erro ao clicar no botao download")

            btn_download = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Download')]"))
            )
            btn_download.click()

            time.sleep(10)

        except Exception as e:
            print(f"Tentando método alternativo...")
            # Tentativa alternativa
            input_url = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='url']"))
            )
            input_url.clear()
            input_url.send_keys(url_video)
            time.sleep(2)

            btn_download = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            btn_download.click()
            time.sleep(1)

        # PASSO 6: Selecionar formato MP4
        # print("Selecionando formato MP4...")
        # try:
        #     # Esperar a página de opções carregar
        #     time.sleep(3)
        #
        #     # Procurar botão de download MP4
        #     btn_mp4 = WebDriverWait(driver, 5).until(
        #         EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'download') and contains(text(), 'MP4')]"))
        #     )
        #     btn_mp4.click()
        #     print("Download MP4 iniciado!")
        #     time.sleep(30)
        #
        # except Exception as e:
        #     print(f"Tentando alternativa para MP4...")
        #     try:
        #         # Algumas versões do site usam botões diferentes
        #         btn_mp4 = WebDriverWait(driver, 3).until(
        #             EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'MP4')]"))
        #         )
        #         btn_mp4.click()
        #         time.sleep(1)
        #
        #         # Clicar no link de download que aparece
        #         link_download = WebDriverWait(driver, 3).until(
        #             EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'download')]"))
        #         )
        #         link_download.click()
        #         print("Download MP4 iniciado!")
        #         time.sleep(30)
        #
        #     except Exception as e:
        #         print(f"Erro ao baixar MP4: {e}")
        #         # Tenta baixar em MP3 se MP4 não funcionar
        #         try:
        #             btn_mp3 = WebDriverWait(driver, 3).until(
        #                 EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'MP3')]"))
        #             )
        #             btn_mp3.click()
        #             print("Download MP3 iniciado!")
        #             time.sleep(30)
        #         except:
        #             print("Não foi possível iniciar o download.")

        # PASSO 7: Verificar se o download começou

        print("\nVerificando download...")
        downloads_path = os.path.expanduser("~/Downloads")
        time.sleep(3)

        # Listar arquivos recentes na pasta Downloads
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

        print("\nProcesso concluído! O navegador permanecerá aberto por 30 segundos.")
        time.sleep(30)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        print("\nDica: O site y2meta pode ter mudado sua interface. ")
        print("Tente acessar manualmente: https://y2meta.is/pt")
        print("Cole a URL: " + (url_video if 'url_video' in locals() else "URL não capturada"))

    finally:
        print("\nFechando navegador...")
        driver.quit()


def baixar_musica_simples():
    """
    Versão mais simples que abre manualmente o YouTube e copia a URL
    """
    print("=== VERSÃO SIMPLES ===\n")
    print("1. O navegador vai abrir o YouTube")
    print("2. Você precisa pesquisar manualmente 'Gorillaz Clint Eastwood'")
    print("3. Copie a URL do vídeo")
    print("4. O script vai abrir o y2meta para você")
    print("5. Cole a URL e baixe o MP4")
    print("\nPressione Enter para continuar...")
    input()

    # Configuração do Chrome
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Abrir YouTube
        print("Abrindo YouTube...")
        driver.get("https://www.youtube.com")
        print("\nPesquise pelo vídeo manualmente e depois cole a URL abaixo.")
        print("Ou pressione Enter para pular para o y2meta.")

        url_video = input("\nCole a URL do vídeo (ou pressione Enter para pular): ")

        if url_video:
            # Abrir y2meta
            driver.execute_script("window.open('https://y2meta.is/pt');")
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[1])

            print("\nCole a URL no y2meta e faça o download manualmente.")
            input("Pressione Enter quando terminar...")
        else:
            print("Abrindo y2meta...")
            driver.get("https://y2meta.is/pt")
            print("Faça o download manualmente.")
            input("Pressione Enter quando terminar...")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    print("=== DOWNLOAD DE MÚSICA DO YOUTUBE ===\n")
    print("Escolha uma opção:")
    print("1 - Automático (tenta baixar automaticamente)")
    print("2 - Semiautomático (você copia a URL)")

    opcao = input("\nOpção (1 ou 2): ")

    if opcao == '2':
        baixar_musica_simples()
    else:
        baixar_musica()