# CRIADOR DE ATALHO DE IPONTO - CAMINHO CORRIGIDO
# --- CONFIGURAÇÕES ---
# Caminho exato do ícone na rede
$serverIconPath = "\\192.168.1.15\comp.marcos\IPONTO"
$shortcutName = "IPONTO.url"
$localIconName = "icone.ico" # Salvando como .ico localmente para o Windows não rejeitar
$url = "https://ipontomobile.com.br/iponto_web/"

# Pasta local (Usando a pasta Pública para evitar bloqueios do OneDrive)
$localFolder = "$env:PUBLIC\IPONTO"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$localShortcut = Join-Path $localFolder $shortcutName
$localIcon = Join-Path $localFolder $localIconName

# --- 1. CRIAÇÃO DA PASTA LOCAL ---
if (!(Test-Path $localFolder)) {
    New-Item -ItemType Directory -Path $localFolder -Force | Out-Null
}

# --- 2. CÓPIA DO ÍCONE DA REDE ---
Write-Host "Buscando o ícone na pasta IPONTO\DADOS..." -ForegroundColor Cyan
try {
    # Copia o arquivo .icon da rede e já salva como .ico na máquina
    Copy-Item $serverIconPath -Destination $localIcon -Force -ErrorAction Stop
} catch {
    Write-Host ""
    Write-Host "ERRO: O arquivo não foi encontrado!" -ForegroundColor Red
    Write-Host "Verifique se este caminho está correto e acessível: $serverIconPath" -ForegroundColor Yellow
    Read-Host "Pressione ENTER para sair"
    exit
}

Write-Host "Ícone copiado com sucesso! Criando atalho..." -ForegroundColor Green

# --- 3. CRIAÇÃO DO ATALHO ---
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($localShortcut)
$shortcut.TargetPath = $url
# O ",0" garante que pegue o índice correto da imagem
$shortcut.IconLocation = "$localIcon,0" 
$shortcut.Save()

# --- 4. COPIAR PARA A ÁREA DE TRABALHO ---
$finalDesktopShortcut = Join-Path $desktopPath $shortcutName
Copy-Item $localShortcut -Destination $finalDesktopShortcut -Force

# --- 5. FORÇAR ATUALIZAÇÃO DO CACHE DE ÍCONES ---
# Isso avisa o Windows Explorer para mostrar o ícone na hora
ie4uinit.exe -show
$code = @'
[DllImport("shell32.dll", CharSet = CharSet.Auto, SetLastError = true)]
public static extern void SHChangeNotify(uint wEventId, uint uFlags, IntPtr dwItem1, IntPtr dwItem2);
'@
$type = Add-Type -MemberDefinition $code -Name "Shell32" -Namespace "Win32" -PassThru
$type::SHChangeNotify(0x08000000, 0x0000, [IntPtr]::Zero, [IntPtr]::Zero)

# --- 6. FINALIZAÇÃO ---
Write-Host "Operação concluída com sucesso! Abrindo IPONTO..." -ForegroundColor Cyan
Start-Process $url

Start-Sleep -Seconds 2
exit