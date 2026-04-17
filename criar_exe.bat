@'
@echo off
echo ========================================
echo    CRIANDO LEANFLOW.EXE
echo ========================================
echo.

echo 1. Usando metodo alternativo...
python -m PyInstaller --onefile --windowed --icon=icon.ico --name="LeanFlow" main.py

echo.
echo ========================================
echo    PRONTO! 🎉
echo ========================================
echo Seu executavel esta em: dist\LeanFlow.exe
echo.
echo Pressione qualquer tecla para abrir a pasta...
pause

explorer dist
'@ | Out-File -FilePath "criar_exe.bat" -Encoding utf8 -Force