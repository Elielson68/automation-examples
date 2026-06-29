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

            # ====================================================
            # NOVA PARTE: RESOLVER O PROBLEMA DO "Loading..."
            # ====================================================
            print("\nAguardando o carregamento dos botões de download...")

            # Esperar o elemento "Loading..." aparecer
            try:
                # Aguarda o texto "Loading..." aparecer
                loading_element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Loading')]"))
                )
                print("Elemento 'Loading...' encontrado!")

                # Obtém a posição do elemento
                location = loading_element.location
                size = loading_element.size

                # Calcula o centro do elemento
                center_x = location['x'] + size['width'] // 2
                center_y = location['y'] + size['height'] // 2

                print(f"Posição do Loading: X={center_x}, Y={center_y}")

                # Move o mouse para o centro do elemento "Loading..."
                pyautogui.moveTo(center_x, center_y, duration=1)
                print("Mouse posicionado sobre 'Loading...'")

                # Aguarda 10 segundos com o mouse parado
                print("Aguardando 10 segundos para os botões aparecerem...")
                for i in range(10, 0, -1):
                    print(f"{i}...", end=" ", flush=True)
                    time.sleep(1)
                print("\nTempo aguardado!")

            except Exception as e:
                print(f"Elemento 'Loading...' não encontrado ou já passou. Continuando...")
                print(f"Erro: {e}")

                # Fallback: se não encontrar o "Loading...", tenta encontrar os botões de download
                print("Tentando encontrar diretamente os botões de download...")

            # Pequena pausa extra
            time.sleep(2)

            # Clicar no botão de download
            btn_download = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Download')]"))
            )
            btn_download.click()
            time.sleep(5)

        except Exception as e:
            print(f"Tentando método alternativo...")
            input_url = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='url']"))
            )
            input_url.clear()
            input_url.send_keys(url_video)
            time.sleep(2)

            btn_download = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            btn_download.click()
            time.sleep(5)



        # PASSO 6: Selecionar formato MP4
        # print("\nSelecionando formato MP4...")
        # try:
        #     # Aguarda os botões de download aparecerem
        #     time.sleep(3)
        #
        #     # Procura por botões MP4 (agora devem estar visíveis)
        #     btn_mp4 = WebDriverWait(driver, 20).until(
        #         EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'download') and contains(text(), 'MP4')]"))
        #     )
        #
        #     # Move o mouse para o botão MP4 antes de clicar
        #     location = btn_mp4.location
        #     size = btn_mp4.size
        #     center_x = location['x'] + size['width'] // 2
        #     center_y = location['y'] + size['height'] // 2
        #     pyautogui.moveTo(center_x, center_y, duration=0.5)
        #     time.sleep(0.5)
        #
        #     btn_mp4.click()
        #     print("Download MP4 iniciado!")
        #     time.sleep(10)
        #
        # except Exception as e:
        #     print(f"Tentando alternativa para MP4...")
        #     try:
        #         # Outra forma de encontrar o botão MP4
        #         btn_mp4 = WebDriverWait(driver, 15).until(
        #             EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'MP4')]"))
        #         )
        #
        #         # Move o mouse para o botão MP4
        #         location = btn_mp4.location
        #         size = btn_mp4.size
        #         center_x = location['x'] + size['width'] // 2
        #         center_y = location['y'] + size['height'] // 2
        #         pyautogui.moveTo(center_x, center_y, duration=0.5)
        #         time.sleep(0.5)
        #
        #         btn_mp4.click()
        #         time.sleep(3)
        #
        #         # Clicar no link de download que aparece
        #         link_download = WebDriverWait(driver, 10).until(
        #             EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'download')]"))
        #         )
        #
        #         # Move o mouse para o link de download
        #         location = link_download.location
        #         size = link_download.size
        #         center_x = location['x'] + size['width'] // 2
        #         center_y = location['y'] + size['height'] // 2
        #         pyautogui.moveTo(center_x, center_y, duration=0.5)
        #         time.sleep(0.5)
        #
        #         link_download.click()
        #         print("Download MP4 iniciado!")
        #         time.sleep(10)
        #
        #     except Exception as e:
        #         print(f"Erro ao baixar MP4: {e}")
        #         # Tenta baixar em MP3 se MP4 não funcionar
        #         try:
        #             btn_mp3 = WebDriverWait(driver, 10).until(
        #                 EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'MP3')]"))
        #             )
        #
        #             # Move o mouse para o botão MP3
        #             location = btn_mp3.location
        #             size = btn_mp3.size
        #             center_x = location['x'] + size['width'] // 2
        #             center_y = location['y'] + size['height'] // 2
        #             pyautogui.moveTo(center_x, center_y, duration=0.5)
        #             time.sleep(0.5)
        #
        #             btn_mp3.click()
        #             print("Download MP3 iniciado!")
        #             time.sleep(10)
        #         except:
        #             print("Não foi possível iniciar o download.")

        # PASSO 7: Verificar o download
        print("\nVerificando download...")
        downloads_path = os.path.expanduser("~/Downloads")
        time.sleep(5)

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
        print("\nDica: O site y2meta pode ter mudado sua interface.")
        print("Tente acessar manualmente: https://y2meta.is/pt")
        if 'url_video' in locals():
            print(f"URL do vídeo: {url_video}")

    finally:
        print("\nFechando navegador...")
        driver.quit()


if __name__ == "__main__":
    baixar_musica()