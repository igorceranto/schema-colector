@echo off
echo Iniciando processo de build...

:: Criar ambiente virtual (se não existir)
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

:: Ativar ambiente virtual
call venv\Scripts\activate.bat

:: Instalar dependências
echo Instalando dependencias...
pip install -r requirements.txt
pip install pyinstaller

:: Limpar builds anteriores
echo Limpando builds anteriores...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del *.spec

:: Gerar executável
echo Gerando executavel...
python -m PyInstaller --onefile --windowed --name "Schema Collector" schema_collector_gui.py

:: Desativar ambiente virtual
call venv\Scripts\deactivate.bat

echo Build concluido!
echo O executavel esta disponivel em: dist\Schema Collector.exe
pause 