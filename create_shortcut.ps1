$WshShell = New-Object -ComObject WScript.Shell
$WorkspacePath = "C:\Users\nites\Documents\ExpertByAi\system-controlAi"
$ChromeExe = "C:\Program Files\Google\Chrome\Application\chrome.exe"

$DesktopTargets = @(
    [System.Environment]::GetFolderPath('Desktop'),
    (Join-Path $env:USERPROFILE "Desktop"),
    (Join-Path $env:USERPROFILE "OneDrive\Desktop")
) | Select-Object -Unique | Where-Object { Test-Path $_ }

foreach ($DesktopPath in $DesktopTargets) {
    $JobShortcutPath = Join-Path $DesktopPath "System Control AI - Job Agent.lnk"
    $JobShortcut = $WshShell.CreateShortcut($JobShortcutPath)
    $JobShortcut.TargetPath = Join-Path $WorkspacePath "launch_job_application_agent.bat"
    $JobShortcut.WorkingDirectory = $WorkspacePath
    $JobShortcut.Description = "1-Click Launch: Chrome (Profile 9) + System Control AI Job Agent"
    if (Test-Path $ChromeExe) {
        $JobShortcut.IconLocation = "$ChromeExe,0"
    } else {
        $JobShortcut.IconLocation = "C:\Windows\System32\shell32.dll,14"
    }
    $JobShortcut.Save()
    Write-Output "Created: $JobShortcutPath"

    $MainShortcutPath = Join-Path $DesktopPath "System Control AI.lnk"
    $MainShortcut = $WshShell.CreateShortcut($MainShortcutPath)
    $MainShortcut.TargetPath = Join-Path $WorkspacePath "launch_system_control.bat"
    $MainShortcut.WorkingDirectory = $WorkspacePath
    $MainShortcut.Description = "Launch System Control AI Interactive Menu (Hybrid/Local/Cloud)"
    $MainShortcut.IconLocation = "C:\Windows\System32\shell32.dll,220"
    $MainShortcut.Save()
    Write-Output "Created: $MainShortcutPath"
}
