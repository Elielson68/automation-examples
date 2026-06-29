import pyautogui
import time

# Configuração de segurança (pausa entre ações)
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True  # Mova o mouse para o canto superior esquerdo para cancelar

print("Movendo o mouse... (Pressione Ctrl+C para cancelar)")

# Espera 3 segundos para você se preparar
time.sleep(1)

# 1. Movimento da esquerda para direita
print("Movendo da esquerda para direita...")
for x in range(100, 900, 20):
    pyautogui.moveTo(x, 400, duration=0.01)

time.sleep(1)

# 2. Movimento de cima para baixo
print("Movendo de cima para baixo...")
for y in range(100, 700, 20):
    pyautogui.moveTo(500, y, duration=0.01)

time.sleep(1)

# 3. Movimento em círculo
print("Movendo em círculo...")
import math

center_x, center_y = 500, 400
radius = 150

for angle in range(0, 361, 5):
    x = center_x + radius * math.cos(math.radians(angle))
    y = center_y + radius * math.sin(math.radians(angle))
    pyautogui.moveTo(x, y, duration=0.02)

print("Movimentos concluídos!")