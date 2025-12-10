import time
import subprocess
import os
import platform
from datetime import datetime

# --- CONFIGURACOES ---
#Coloque o nome que aparece no gerenciador de tarefas, para encerrar a tarefa
NOME_PROCESSO = "X"
#Coloque o camiho do programa na pasta riz dele (atalhos podem funcionar, mas nao e o ideal)
CAMINHO_PROGRAMA = r"X"

# Lista de horarios (formato 24h, adicione quantos quiser separados por virgula)
LISTA_HORARIOS = ["15:15"] 
# ---------------------

def reiniciar():
    sistema = platform.system()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando reinicializacao do {NOME_PROCESSO}...")
    
    # 1. Fechar o programa
    try:
        if sistema == "Windows":
            # /F forca, /IM nome da imagem. O >nul oculta msg de erro se nao estiver aberto
            os.system(f"taskkill /F /IM {NOME_PROCESSO} >nul 2>&1")
        else:
            os.system(f"pkill -f {NOME_PROCESSO}")
    except Exception as e:
        print(f"Erro ao fechar (pode ja estar fechado): {e}")
    
    # Espera um pouco para garantir que o SO liberou o arquivo
    time.sleep(5)
    
    # 2. Abrir o programa
    try:
        subprocess.Popen(CAMINHO_PROGRAMA)
        print("Programa reaberto com sucesso.")
    except Exception as e:
        print(f"Erro ao abrir o programa: {e}")

print(f"Script rodando! Monitorando os horarios: {LISTA_HORARIOS}")

# Variavel para controlar qual foi o ultimo horario executado para nao repetir no mesmo minuto
ultimo_horario_executado = ""

while True:
    agora = datetime.now()
    hora_atual = agora.strftime("%H:%M")

    # Verifica se a hora atual esta na sua lista E se ja nao executamos ela agora
    if hora_atual in LISTA_HORARIOS and hora_atual != ultimo_horario_executado:
        reiniciar()
        # Marca que este horario ja foi processado
        ultimo_horario_executado = hora_atual
    
    # Resetar a variavel se o horario mudou, para garantir que no dia seguinte funcione
    # (Se a hora atual nao esta na lista, limpam o buffer de "ultimo executado")
    if hora_atual not in LISTA_HORARIOS:
        ultimo_horario_executado = ""

    # Verifica a cada 10 segundos. (nao pesa na cpu!)
    time.sleep(10)