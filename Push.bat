@echo off
REM ================================
REM Auto Git Push Script
REM ================================

REM Set repo folder path here
set REPO_PATH=C:\path\to\your\repo

REM Commit message (default = "Auto commit")
set COMMIT_MSG=Auto commit

REM If you want to pass a commit message as an argument, use %1
if not "%~1"=="" (
    set COMMIT_MSG=%*
)

echo ---------------------------------
echo Navigating to repository folder...
cd /d "%REPO_PATH%"

echo Adding changes...
git add .

echo Committing changes with message: "%COMMIT_MSG%"
git commit -m "%COMMIT_MSG%"

echo Pushing to remote...
git push origin main

echo Done!
pause