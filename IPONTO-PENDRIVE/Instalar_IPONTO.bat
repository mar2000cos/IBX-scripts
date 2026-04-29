@echo off
:: O comando %~dp0 garante que o .bat procure o script na mesma pasta do pendrive
powershell.exe -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File "%~dp0Criador_IPONTO.ps1"
exit