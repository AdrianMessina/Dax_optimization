# Script para crear acceso directo a DAX Optimizer v1.1

$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = "$Desktop\DAX Optimizer v1.1.lnk"
$TargetPath = "$PSScriptRoot\run_dax_optimizer.bat"
$IconLocation = "C:\Windows\System32\shell32.dll,165"

# Crear acceso directo
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.IconLocation = $IconLocation
$Shortcut.Description = "DAX Optimizer v1.1 - Analizador de archivos PBIP"
$Shortcut.Save()

Write-Host "Acceso directo creado en el escritorio!" -ForegroundColor Green
Write-Host "Ruta: $ShortcutPath" -ForegroundColor Cyan

Start-Sleep -Seconds 2
