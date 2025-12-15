import time
import subprocess
import os
import platform
import ctypes 
import json
import msvcrt  # Biblioteca para detectar teclas no Windows
from datetime import datetime

# --- CONFIGURACOES ---

# Caminho do Java
CAMINHO_JAVA = r"C:\SEAT\TVExperience\java\jre1.8.0_66\bin\javaw.exe"

# Lista de programas para abrir
LISTA_PROGRAMAS = [
    r"C:\SEAT\TVExperience\tv-experience.jar",
    r"C:\SEAT\Setores\setores-servidor-6.2.2.jar"
]

# Nome do processo para fechar
NOME_PROCESSO = "javaw.exe"

# Arquivo para salvar os horarios configurados
ARQUIVO_CONFIG = "config_horarios.json"

# ---------------------

def carregar_horarios():
    """Carrega os horarios do arquivo JSON ou usa o padrao."""
    if os.path.exists(ARQUIVO_CONFIG):
        try:
            with open(ARQUIVO_CONFIG, 'r') as f:
                dados = json.load(f)
                return dados.get("horarios", ["12:55"])
        except:
            return ["12:55"]
    else:
        return ["12:55"]

def salvar_horarios(lista_novos_horarios):
    """Salva a lista de horarios no arquivo JSON."""
    try:
        with open(ARQUIVO_CONFIG, 'w') as f:
            json.dump({"horarios": lista_novos_horarios}, f)
        print("Configuracao salva com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar config: {e}")

# Carrega os horarios iniciais
LISTA_HORARIOS = carregar_horarios()

def minimizar_console():
    """Minimiza a janela do console."""
    if platform.system() == "Windows":
        try:
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 6) # 6 = Minimizar
        except Exception as e:
            print(f"Nao foi possivel minimizar: {e}")

def mostrar_console():
    """Restaura a janela do console para o usuario ver o menu."""
    if platform.system() == "Windows":
        try:
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 9) # 9 = Restaurar
                ctypes.windll.user32.SetForegroundWindow(whnd) # Traz para frente
        except:
            pass

def reiniciar():
    sistema = platform.system()
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] --- INICIANDO REINICIALIZACAO GERAL ---")
    
    # --- ETAPA 1: FECHAR TUDO ---
    print(f"Fechando processos {NOME_PROCESSO}...")
    try:
        if sistema == "Windows":
            os.system(f"taskkill /F /IM {NOME_PROCESSO} >nul 2>&1")
        else:
            os.system(f"pkill -f {NOME_PROCESSO}")
    except Exception as e:
        print(f"Aviso ao fechar: {e}")
    
    time.sleep(5)
    
    # --- ETAPA 2: ABRIR CADA PROGRAMA DA LISTA ---
    for caminho_jar in LISTA_PROGRAMAS:
        try:
            pasta_do_arquivo = os.path.dirname(caminho_jar)
            print(f"Abrindo: {os.path.basename(caminho_jar)}...")
            comando = [CAMINHO_JAVA, "-jar", caminho_jar]
            subprocess.Popen(comando, cwd=pasta_do_arquivo)
            time.sleep(2)
        except Exception as e:
            print(f"ERRO ao abrir {caminho_jar}: {e}")

    print("Todos os programas foram reiniciados.\n")

def menu_configuracao():
    """Exibe o menu para alterar horarios."""
    global LISTA_HORARIOS
    mostrar_console()
    os.system('cls') # Limpa a tela
    print("====================================")
    print("      CONFIGURACAO DE HORARIOS      ")
    print("====================================")
    print(f"Horarios Atuais: {LISTA_HORARIOS}")
    print("1 - Mudar horario (Apaga tudo e define um novo)")
    print("2 - Adicionar novo horario (Mantem os atuais)")
    print("3 - Cancelar e voltar a monitorar")
    print("====================================")
    
    opcao = input("Escolha uma opcao: ")

    if opcao == "1":
        novo = input("Digite o novo horario (HH:MM): ")
        if len(novo) == 5 and ":" in novo:
            LISTA_HORARIOS = [novo]
            salvar_horarios(LISTA_HORARIOS)
            print(f"Horario redefinido para: {LISTA_HORARIOS}")
        else:
            print("Formato invalido! Use HH:MM")
            time.sleep(2)

    elif opcao == "2":
        novo = input("Digite o horario para adicionar (HH:MM): ")
        if len(novo) == 5 and ":" in novo:
            if novo not in LISTA_HORARIOS:
                LISTA_HORARIOS.append(novo)
                salvar_horarios(LISTA_HORARIOS)
                print(f"Horario adicionado! Lista atual: {LISTA_HORARIOS}")
            else:
                print("Horario ja existe na lista.")
        else:
            print("Formato invalido! Use HH:MM")
            time.sleep(2)
            
    elif opcao == "3":
        print("Voltando...")
    
    else:
        print("Opcao invalida.")

    print("Minimizando em 3 segundos...")
    time.sleep(3)
    minimizar_console()

# --- INICIO DO SCRIPT ---

minimizar_console()
print(f"Script rodando! Pressione 'M' para configurar.")
print(f"Monitorando horarios: {LISTA_HORARIOS}")

ultimo_horario_executado = ""

while True:
    agora = datetime.now()
    hora_atual = agora.strftime("%H:%M")

    # 1. Checagem de horario para reiniciar
    if hora_atual in LISTA_HORARIOS and hora_atual != ultimo_horario_executado:
        reiniciar()
        ultimo_horario_executado = hora_atual
    
    if hora_atual not in LISTA_HORARIOS:
        ultimo_horario_executado = ""

    # 2. Checagem se a tecla 'M' foi pressionada (Sem travar o script)
    if msvcrt.kbhit(): # Se alguma tecla foi apertada
        tecla = msvcrt.getch() # Le a tecla
        if tecla.lower() == b'm': # Se for 'm' ou 'M'
            menu_configuracao()

    # Sleep menor para o teclado responder mais rapido
    time.sleep(0.5)