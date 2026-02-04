# Script para crear acceso directo a DAX Optimizer v1.1 en el escritorio
# Este script NO reemplaza accesos directos existentes

$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = "$Desktop\DAX Optimizer v1.1.lnk"
$TargetPath = "$PSScriptRoot\run_dax_optimizer.bat"
$IconLocation = "C:\Windows\System32\shell32.dll,165"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DAX Optimizer v1.1" -ForegroundColor Yellow
Write-Host "  Crear acceso directo" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si ya existe un acceso directo
if (Test-Path $ShortcutPath) {
    Write-Host "Ya existe un acceso directo en:" -ForegroundColor Yellow
    Write-Host "  $ShortcutPath" -ForegroundColor White
    Write-Host ""
    $response = Read-Host "Deseas reemplazarlo? (S/N)"

    if ($response -ne "S" -and $response -ne "s") {
        Write-Host "Operacion cancelada." -ForegroundColor Red
        Start-Sleep -Seconds 2
        exit
    }

    Remove-Item $ShortcutPath -Force
    Write-Host "Acceso directo anterior eliminado." -ForegroundColor Green
}

# Crear acceso directo
Write-Host "Creando acceso directo..." -ForegroundColor Cyan
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.IconLocation = $IconLocation
$Shortcut.Description = "DAX Optimizer v1.1 - Analizador completo de archivos PBIP"
$Shortcut.Save()

Write-Host ""
Write-Host "Acceso directo creado exitosamente!" -ForegroundColor Green
Write-Host "Ubicacion: $Desktop" -ForegroundColor Cyan
Write-Host "Nombre: DAX Optimizer v1.1.lnk" -ForegroundColor Cyan
Write-Host ""
Write-Host "Haz doble clic en el acceso directo para iniciar la aplicacion." -ForegroundColor Yellow

Start-Sleep -Seconds 3
