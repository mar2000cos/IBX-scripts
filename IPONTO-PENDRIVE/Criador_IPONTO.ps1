# O $PSScriptRoot pega automaticamente a pasta atual do pendrive de onde o script está rodando
$pendrivePath = $PSScriptRoot
$serverIconPath = Join-Path $pendrivePath "icone.icon"

# Configurações do atalho
$shortcutName = "IPONTO.lnk"
$localIconName = "icone.ico"
$url = "https://ipontomobile.com.br/iponto_web/"

# Pasta local na máquina do cliente (Pasta Pública)
$localFolder = "$env:PUBLIC\IPONTO"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$localShortcut = Join-Path $localFolder $shortcutName
$localIcon = Join-Path $localFolder $localIconName

# --- 1. CRIAÇÃO DA PASTA LOCAL ---
if (!(Test-Path $localFolder)) {
    New-Item -ItemType Directory -Path $localFolder -Force | Out-Null
}

# --- 2. CÓPIA DO ÍCONE DO PENDRIVE PARA A MÁQUINA ---
try {
    # Copia o arquivo .icon do pendrive e salva como .ico na máquina
    Copy-Item $serverIconPath -Destination $localIcon -Force -ErrorAction Stop
} catch {
    # Em um pendrive, o WindowStyle Hidden do .bat vai esconder essa tela, 
    # mas mantemos por segurança caso rode manualmente.
    exit
}

# --- 3. CRIAÇÃO DO ATALHO ---
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($localShortcut)
$shortcut.TargetPath = $url
$shortcut.IconLocation = "$localIcon,0" 
$shortcut.Save()

# --- 4. COPIAR PARA A ÁREA DE TRABALHO ---
$finalDesktopShortcut = Join-Path $desktopPath $shortcutName
Copy-Item $localShortcut -Destination $finalDesktopShortcut -Force

# --- 5. FORÇAR ATUALIZAÇÃO DO CACHE DE ÍCONES ---
ie4uinit.exe -show
$code = @'
[DllImport("shell32.dll", CharSet = CharSet.Auto, SetLastError = true)]
public static extern void SHChangeNotify(uint wEventId, uint uFlags, IntPtr dwItem1, IntPtr dwItem2);
'@
$type = Add-Type -MemberDefinition $code -Name "Shell32" -Namespace "Win32" -PassThru
$type::SHChangeNotify(0x08000000, 0x0000, [IntPtr]::Zero, [IntPtr]::Zero)

# --- 6. FINALIZAÇÃO ---
Start-Process $url
exit