#CRIADOR DE ATALHO DE CHAMADO ti
# --- CONFIGURAÇÕES ---
$serverPath = "\\192.168.1.15\comp.marcos"
$shortcutName = "Chamados TI.url" # Nome do arquivo de atalho na rede
$iconName = "logo2.ico"     # Nome do arquivo de ícone na rede
$url = "http://192.168.1.247/glpi/index.php?redirect=%2Ffront%2Fcentral.php&error=3" # URL que o atalho deve abrir

# Caminhos locais
$localFolder = Join-Path $env:USERPROFILE "Documents\LGPI"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$localShortcut = Join-Path $localFolder $shortcutName
$localIcon = Join-Path $localFolder $iconName

# --- 1. CRIAÇÃO DA PASTA LOCAL ---
if (!(Test-Path $localFolder)) {
    New-Item -ItemType Directory -Path $localFolder -Force
}

# --- 2. CÓPIA DOS ARQUIVOS DA REDE ---
Write-Host "Copiando arquivos da rede..." -ForegroundColor Cyan
try {
    Copy-Item "$serverPath\$iconName" -Destination $localIcon -Force
    # Se o atalho já existir na rede, copiamos. Se não, o script cria um novo abaixo.
    if (Test-Path "$serverPath\$shortcutName") {
        Copy-Item "$serverPath\$shortcutName" -Destination $localShortcut -Force
    }
} catch {
    Write-Error "Erro ao acessar a rede. Verifique as permissões em $serverPath"
    exit
}

# --- 3. CRIAÇÃO/CONFIGURAÇÃO DO ATALHO COM ÍCONE ---
$shell = New-Object -ComObject WScript.Shell

# Criar/Configurar na pasta Documentos\LGPI
$shortcut = $shell.CreateShortcut($localShortcut)
$shortcut.TargetPath = $url
$shortcut.IconLocation = $localIcon
$shortcut.Save()

# --- 4. COPIAR PARA A ÁREA DE TRABALHO ---
Copy-Item $localShortcut -Destination (Join-Path $desktopPath $shortcutName) -Force

# --- 5. ABRIR A PÁGINA WEB ---
Write-Host "Abrindo a página web..." -ForegroundColor Green
Start-Process $url

Write-Host "Operação concluída com sucesso!" -ForegroundColor Green

# Força o fechamento da janela do PowerShell
exit