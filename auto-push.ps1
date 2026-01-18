# Auto-commit and push script for skin disease project
# This script should be run in the project directory whenever changes are made

param(
    [string]$message = "Auto-update from VS Code"
)

# Navigate to project directory
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if there are any changes
$gitStatus = & git -C $projectPath status --porcelain
if ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Write-Host "No changes to commit."
    exit 0
}

# Add all changes
Write-Host "Adding files..."
& git -C $projectPath add -A

# Commit
Write-Host "Committing changes with message: $message"
& git -C $projectPath commit -m $message

# Push
Write-Host "Pushing to GitHub..."
& git -C $projectPath push -u origin main
if ($LASTEXITCODE -eq 128) {
    Write-Host "Branch 'main' doesn't exist on remote. Trying 'master'..."
    & git -C $projectPath push -u origin master
}

Write-Host "Done!"
