"""
Manipulação dos comandos de som do sistema operacional usando Python.
"""

import winsound
import time
import random


def bip_simples():
    """Emite um bip simples"""
    winsound.Beep(1000, 200)  # Frequência de 1000Hz por 200ms


def bip_multiplo(vezes=3):
    """Emite múltiplos bips"""
    for i in range(vezes):
        winsound.Beep(800, 150)
        time.sleep(0.1)


def bip_musica():
    """Emite uma sequência musical simples"""
    notas = [440, 494, 523, 587, 659, 740, 784, 880]  # Notas musicais

    for nota in notas:
        winsound.Beep(nota, 200)
        time.sleep(0.1)


def bip_alerta():
    """Emite um som de alerta variado"""
    for _ in range(3):
        # Aumenta e diminui a frequência
        for freq in range(500, 1500, 100):
            winsound.Beep(freq, 50)
        time.sleep(0.1)
        for freq in range(1500, 500, -100):
            winsound.Beep(freq, 50)
        time.sleep(0.2)


def main():
    print("=== GERADOR DE SONS ===")
    print("1 - Bip simples")
    print("2 - Bip múltiplo")
    print("3 - Música simples")
    print("4 - Som de alerta")
    print("5 - Som aleatório")

    opcao = input("Escolha uma opção (1-5): ")

    try:
        if opcao == '1':
            print("Emiitndo bip...")
            bip_simples()

        elif opcao == '2':
            vezes = int(input("Quantos bips? "))
            print(f"Emiitndo {vezes} bips...")
            bip_multiplo(vezes)

        elif opcao == '3':
            print("Tocando música...")
            bip_musica()

        elif opcao == '4':
            print("Som de alerta...")
            bip_alerta()

        elif opcao == '5':
            print("Som aleatório...")
            for _ in range(10):
                freq = random.randint(300, 2000)
                duracao = random.randint(50, 300)
                winsound.Beep(freq, duracao)
                time.sleep(0.05)
        else:
            print("Opção inválida!")

    except ValueError:
        print("Valor inválido!")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()