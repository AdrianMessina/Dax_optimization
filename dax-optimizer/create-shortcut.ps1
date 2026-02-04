$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\DAX Optimizer.lnk")
$Shortcut.TargetPath = "$PSScriptRoot\start-dax-optimizer.bat"
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.Description = "Analizador y optimizador de codigo DAX para Power BI"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,137"
$Shortcut.Save()

Write-Host "Acceso directo creado exitosamente en el escritorio!" -ForegroundColor Green
