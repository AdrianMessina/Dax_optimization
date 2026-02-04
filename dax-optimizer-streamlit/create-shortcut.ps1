$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut("$env:USERPROFILE\Desktop\DAX Optimizer.lnk")
$Shortcut.TargetPath = "$PSScriptRoot\run_dax_optimizer.bat"
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.Description = "Analizador y optimizador de código DAX para Power BI"
$Shortcut.Save()
Write-Host "Acceso directo creado en el escritorio"
