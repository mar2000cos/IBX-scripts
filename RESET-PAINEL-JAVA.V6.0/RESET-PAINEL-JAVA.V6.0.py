import time
import subprocess
import os
import platform
import ctypes 
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

# 4. Horarios de reinicio
LISTA_HORARIOS = ["12:55"] 

# ---------------------

def minimizar_console():
    """Minimiza a janela do console imediatamente apos iniciar."""
    if platform.system() == "Windows":
        try:
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                # 6 = SW_MINIMIZE (Minimiza a janela e ativa a proxima no Z-order)
                ctypes.windll.user32.ShowWindow(whnd, 6)
                print("Janela minimizada para a barra de tarefas.")
        except Exception as e:
            print(f"Nao foi possivel minimizar: {e}")

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
            # Descobre a pasta onde o jar esta
            pasta_do_arquivo = os.path.dirname(caminho_jar)
            
            print(f"Abrindo: {os.path.basename(caminho_jar)}...")
            
            comando = [CAMINHO_JAVA, "-jar", caminho_jar]
            
            # Abre o programa dentro da pasta dele
            subprocess.Popen(comando, cwd=pasta_do_arquivo)
            
            time.sleep(2)
            
        except Exception as e:
            print(f"ERRO ao abrir {caminho_jar}: {e}")

    print("Todos os programas foram reiniciados.\n")

# --- INICIO DO SCRIPT ---

# Chama a funcao para minimizar assim que comeca
minimizar_console()

print(f"Script rodando minimizado! Monitorando: {LISTA_HORARIOS}")
print(f"Programas configurados: {len(LISTA_PROGRAMAS)}")

ultimo_horario_executado = ""

while True:
    agora = datetime.now()
    hora_atual = agora.strftime("%H:%M")

    if hora_atual in LISTA_HORARIOS and hora_atual != ultimo_horario_executado:
        # Se voce quiser que a janela suba (apareca) quando for reiniciar, 
        # descomente a linha abaixo. Caso contrario, ele fara tudo minimizado.
        # ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 9) 
        
        reiniciar()
        ultimo_horario_executado = hora_atual
    
    if hora_atual not in LISTA_HORARIOS:
        ultimo_horario_executado = ""

    time.sleep(10)