import psutil
import os
import time


def listar_processos(filtro=None):
    """Lista processos ativos com filtro opcional"""
    processos = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            nome = proc.info['name']
            pid = proc.info['pid']

            # Aplica filtro se especificado
            if filtro:
                if filtro.lower() in nome.lower():
                    processos.append(proc)
                    print(f"PID: {pid} - Nome: {nome}")
            else:
                processos.append(proc)
                print(f"PID: {pid} - Nome: {nome}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processos


def fechar_processo(proc):
    """Fecha um processo"""
    try:
        proc.terminate()
        # Aguarda o processo terminar
        time.sleep(2)
        if proc.is_running():
            proc.kill()  # Força o encerramento
        print(f"Processo {proc.info['name']} fechado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao fechar processo: {e}")
        return False


def focar_processo(proc):
    """Tenta trazer o processo para o foco"""
    try:
        # No Windows, podemos usar pygetwindow
        import pygetwindow as gw

        # Tenta encontrar a janela pelo nome do processo
        nome = proc.info['name'].replace('.exe', '')
        janelas = gw.getWindowsWithTitle(nome)

        if janelas:
            janelas[0].activate()
            print(f"Janela do {nome} trazida para o foco!")
        else:
            print(f"Não foi possível encontrar a janela do {nome}")
    except Exception as e:
        print(f"Erro ao focar processo: {e}")


def main():
    print("=== GERENCIADOR DE PROCESSOS ===")

    # Lista processos com filtro
    filtro = input("Digite um termo para filtrar os processos (ou Enter para listar todos): ")

    if filtro:
        print(f"\nProcessos contendo '{filtro}':")
    else:
        print("\nTodos os processos:")

    processos = listar_processos(filtro)

    if not processos:
        print("Nenhum processo encontrado.")
        return

    # Pergunta qual processo gerenciar
    pid_input = input("\nDigite o PID do processo que deseja gerenciar: ")

    try:
        pid = int(pid_input)
        proc_selecionado = None

        for proc in processos:
            if proc.info['pid'] == pid:
                proc_selecionado = proc
                break

        if not proc_selecionado:
            print("Processo não encontrado.")
            return

        print(f"\nProcesso selecionado: {proc_selecionado.info['name']} (PID: {pid})")
        acao = input("Deseja [F]echar ou [M]udar foco? (F/M): ").upper()

        if acao == 'F':
            fechar_processo(proc_selecionado)
        elif acao == 'M':
            focar_processo(proc_selecionado)
        else:
            print("Opção inválida!")

    except ValueError:
        print("PID inválido!")


if __name__ == "__main__":
    main()