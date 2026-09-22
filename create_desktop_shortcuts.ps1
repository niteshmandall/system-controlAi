$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$WorkspacePath = "C:\Users\nites\Documents\ExpertByAi\system-controlAi"

# 1. 1-Click Job Application Agent Shortcut
$JobShortcutPath = Join-Path $DesktopPath "System Control AI - Job Agent.lnk"
$JobShortcut = $WshShell.CreateShortcut($JobShortcutPath)
$JobShortcut.TargetPath = Join-Path $WorkspacePath "launch_job_application_agent.bat"
$JobShortcut.WorkingDirectory = $WorkspacePath
$JobShortcut.Description = "1-Click Launch: Chrome (Profile 9) + System Control AI Job Agent"

# Use Chrome icon if available, otherwise shell icon
$ChromeExe = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (Test-Path $ChromeExe) {
    $JobShortcut.IconLocation = "$ChromeExe,0"
} else {
    $JobShortcut.IconLocation = "C:\Windows\System32\shell32.dll,14"
}
$JobShortcut.Save()
Write-Output "Created: $JobShortcutPath"

# 2. Main System Control AI Menu Shortcut
$MainShortcutPath = Join-Path $DesktopPath "System Control AI.lnk"
$MainShortcut = $WshShell.CreateShortcut($MainShortcutPath)
$MainShortcut.TargetPath = Join-Path $WorkspacePath "launch_system_control.bat"
$MainShortcut.WorkingDirectory = $WorkspacePath
$MainShortcut.Description = "Launch System Control AI Interactive Menu (Hybrid/Local/Cloud)"
$MainShortcut.IconLocation = "C:\Windows\System32\shell32.dll,220"
$MainShortcut.Save()
Write-Output "Created: $MainShortcutPath"
