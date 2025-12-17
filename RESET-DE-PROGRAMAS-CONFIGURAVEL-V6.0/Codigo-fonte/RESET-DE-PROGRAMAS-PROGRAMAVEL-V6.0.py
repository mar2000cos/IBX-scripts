import time
import subprocess
import os
import platform
import ctypes
import json
import msvcrt
from datetime import datetime

# --- ARQUIVO DE CONFIGURACAO ---
ARQUIVO_CONFIG = "config_reset_v3.json"

# Valores Padrao (caso nao exista config salva)
CONFIG = {
    "nome_processo": "notepad.exe",
    "caminho_programa": r"C:\Windows\System32\notepad.exe",
    "horarios": ["15:15"]
}

# ---------------------

def carregar_config():
    """Carrega as configuracoes do arquivo JSON ou usa o padrao."""
    global CONFIG
    if os.path.exists(ARQUIVO_CONFIG):
        try:
            with open(ARQUIVO_CONFIG, 'r') as f:
                dados = json.load(f)
                CONFIG.update(dados)
        except Exception as e:
            print(f"Erro ao ler config: {e}")
    else:
        salvar_config()

def salvar_config():
    """Salva as configuracoes atuais no arquivo JSON."""
    try:
        with open(ARQUIVO_CONFIG, 'w') as f:
            json.dump(CONFIG, f, indent=4)
        print(" >> Configuracao salva com sucesso!")
        time.sleep(1.5)
    except Exception as e:
        print(f"Erro ao salvar config: {e}")

def minimizar_console():
    """Minimiza a janela do console."""
    if platform.system() == "Windows":
        try:
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 6) # 6 = Minimizar
        except:
            pass

def mostrar_console():
    """Restaura a janela do console."""
    if platform.system() == "Windows":
        try:
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 9) # 9 = Restaurar
                ctypes.windll.user32.SetForegroundWindow(whnd)
        except:
            pass

def imprimir_status_inicial():
    """Funcao auxiliar para mostrar o status na tela limpa"""
    print(f"Script V3.0 rodando! Pressione 'M' para configurar.")
    print(f"Alvo: {CONFIG['nome_processo']} | Horarios: {CONFIG['horarios']}")

def reiniciar():
    sistema = platform.system()
    nome_proc = CONFIG["nome_processo"]
    caminho_prog = CONFIG["caminho_programa"]
    
    # Se a janela estiver minimizada, o usuario nao vera isso a menos que abra
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Iniciando reinicializacao de: {nome_proc}...")
    
    # 1. Fechar o programa
    try:
        if sistema == "Windows":
            os.system(f"taskkill /F /IM \"{nome_proc}\" >nul 2>&1")
        else:
            os.system(f"pkill -f \"{nome_proc}\"")
        print("Comando de fechamento enviado.")
    except Exception as e:
        print(f"Erro ao tentar fechar: {e}")
    
    time.sleep(5)
    
    # 2. Abrir o programa
    try:
        if os.path.exists(caminho_prog):
            subprocess.Popen([caminho_prog]) 
            print(">> SUCESSO: Programa reaberto com sucesso.")
        else:
            print(f"ERRO CRITICO: O arquivo nao foi encontrado em: {caminho_prog}")
    except Exception as e:
        print(f"Erro ao abrir o programa: {e}")

    # --- BLOCO DE RETORNO AO MENU INICIAL ---
    print("\n------------------------------------------------")
    print("Ciclo concluido. Voltando ao monitoramento em 3 segundos...")
    time.sleep(3)
    
    os.system('cls')         # Limpa a tela
    imprimir_status_inicial() # Mostra as informacoes iniciais de novo
    minimizar_console()       # Esconde a janela novamente

def menu_configuracao():
    """Menu interativo conforme solicitado."""
    mostrar_console()
    
    while True:
        os.system('cls')
        print("==========================================")
        print("      CONFIGURACAO DE REINICIALIZACAO     ")
        print("==========================================")
        print(f"Horarios Atuais: {CONFIG['horarios']}")
        print(f"Programa Alvo: {CONFIG['nome_processo']}")
        print("------------------------------------------")
        print("1 - Alterar hora atual (Redefinir)")
        print("2 - Adicionar mais um horario")
        print("3 - Mudar o programa")
        print("4 - Voltar a monitorar (Sair do menu)")
        print("==========================================")
        
        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            print("\n--- ALTERAR HORA ---")
            novo = input("Digite o novo horario (HH:MM): ")
            if ":" in novo and len(novo) == 5:
                CONFIG['horarios'] = [novo]
                salvar_config()
            else:
                print("Formato invalido! Use HH:MM")
                time.sleep(2)

        elif opcao == "2":
            print("\n--- ADICIONAR HORARIO ---")
            novo = input("Digite o horario para adicionar (HH:MM): ")
            if ":" in novo and len(novo) == 5:
                if novo not in CONFIG['horarios']:
                    CONFIG['horarios'].append(novo)
                    salvar_config()
                else:
                    print("Esse horario ja existe.")
                    time.sleep(2)
            else:
                print("Formato invalido! Use HH:MM")
                time.sleep(2)

        elif opcao == "3":
            print("\n--- MUDAR O PROGRAMA ---")
            novo_nome = input("Digite o nome do processo na aba detalhes (Task manager): ").strip()
            if not novo_nome:
                print("Nome invalido, cancelando...")
                time.sleep(2)
                continue

            print("Digite o caminho do programa:")
            print("(Ex: C:\\Pasta\\programa.exe)")
            novo_caminho = input(">> ").strip().replace('"', '')

            if os.path.exists(novo_caminho):
                CONFIG['nome_processo'] = novo_nome
                CONFIG['caminho_programa'] = novo_caminho
                salvar_config()
            else:
                print("\n[ERRO] O caminho informado nao existe ou esta errado.")
                time.sleep(3)

        elif opcao == "4":
            print("Voltando...")
            time.sleep(1)
            # Limpa a tela e mostra o status inicial antes de minimizar
            os.system('cls')
            imprimir_status_inicial()
            minimizar_console()
            break
        
        else:
            print("Opcao invalida.")
            time.sleep(1)

# --- INICIO DO SCRIPT ---

carregar_config()
minimizar_console()
imprimir_status_inicial()

ultimo_horario_executado = ""

while True:
    agora = datetime.now()
    hora_atual = agora.strftime("%H:%M")

    # Verifica Horario
    if hora_atual in CONFIG['horarios'] and hora_atual != ultimo_horario_executado:
        reiniciar()
        ultimo_horario_executado = hora_atual
    
    if hora_atual not in CONFIG['horarios']:
        ultimo_horario_executado = ""

    # Verifica Tecla 'M'
    if msvcrt.kbhit():
        tecla = msvcrt.getch()
        if tecla.lower() == b'm':
            menu_configuracao()

    time.sleep(0.5)