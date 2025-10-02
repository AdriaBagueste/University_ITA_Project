@echo off
REM ================================
REM Auto Git Push Script con Variables
REM ================================

REM Ruta local del repositorio
set REPO_PATH=C:\Branch\Uni\Tercer Quadrimestre\Infrastructures del transport aeri\ITA project

REM Nombre del branch (ej: main, master, dev, etc.)
set BRANCH=main

REM URL de tu repositorio remoto (GitHub)
set REMOTE_URL=https://github.com/AdriaBagueste/University_ITA_Project.git

REM Mensaje de commit por defecto
set COMMIT_MSG=Auto commit

REM Si pasas un mensaje como argumento (%1), lo usa en lugar del default
if not "%~1"=="" (
    set COMMIT_MSG=%*
)

echo ---------------------------------
echo Navegando al repositorio...
cd /d "%REPO_PATH%"
if errorlevel 1 (
    echo Error: No se encontro la carpeta del repo.
    pause
    exit /b 1
)

echo Verificando remote origin...
git remote -v | find "origin" >nul
if errorlevel 1 (
    echo Remote origin no existe, configurando...
    git remote add origin %REMOTE_URL%
)

echo Agregando cambios...
git add .
if errorlevel 1 (
    echo Error al ejecutar git add.
    pause
    exit /b 1
)

echo Commit con mensaje: "%COMMIT_MSG%"
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo No hay cambios para commit o error en git commit.
)

echo ---------------------------------
echo Sincronizando con el remoto...
git pull origin %BRANCH% --rebase
if errorlevel 1 (
    echo Error al ejecutar git pull.
    pause
    exit /b 1
)

echo Pushing al branch "%BRANCH%"...
git push origin %BRANCH%
if errorlevel 1 (
    echo Error al ejecutar git push.
    pause
    exit /b 1
)

echo ---------------------------------
echo Listo. Cambios enviados a GitHub.
pause
