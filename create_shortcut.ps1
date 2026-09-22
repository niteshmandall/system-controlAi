$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$ShortcutPath = Join-Path $DesktopPath "System Control AI.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\nites\Documents\ExpertByAi\system-controlAi\launch_system_control.bat"
$Shortcut.WorkingDirectory = "C:\Users\nites\Documents\ExpertByAi\system-controlAi"
$Shortcut.Description = "Launch System Control AI Autonomous Agent"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,220"
$Shortcut.Save()
Write-Output "Created shortcut: $ShortcutPath"
