# Configuração de execução
$ErrorActionPreference = "Stop"

Write-Host "Iniciando processo de build..." -ForegroundColor Green

# Função para verificar se um comando existe
function Test-Command {
    param ($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try { if (Get-Command $command) { return $true } }
    catch { return $false }
    finally { $ErrorActionPreference = $oldPreference }
}

# Verificar se Python está instalado
if (-not (Test-Command python)) {
    Write-Host "Python não encontrado! Por favor, instale o Python 3.x." -ForegroundColor Red
    exit 1
}

# Criar ambiente virtual (se não existir)
if (-not (Test-Path "venv")) {
    Write-Host "Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv venv
}

# Ativar ambiente virtual
Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Atualizar pip
Write-Host "Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Instalar dependências
Write-Host "Instalando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt
pip install pyinstaller

# Fechar processos que possam estar usando os arquivos
Write-Host "Verificando processos..." -ForegroundColor Yellow
Get-Process | Where-Object { $_.Path -like "*schema_colector_gui*" } | Stop-Process -Force -ErrorAction SilentlyContinue

# Aguardar um momento para garantir que os arquivos foram liberados
Start-Sleep -Seconds 2

# Limpar builds anteriores
Write-Host "Limpando builds anteriores..." -ForegroundColor Yellow
if (Test-Path "build") { 
    try { Remove-Item -Path "build" -Recurse -Force -ErrorAction Stop }
    catch { Write-Host "Não foi possível remover a pasta build. Continuando..." -ForegroundColor Yellow }
}
if (Test-Path "dist") { 
    try { Remove-Item -Path "dist" -Recurse -Force -ErrorAction Stop }
    catch { Write-Host "Não foi possível remover a pasta dist. Continuando..." -ForegroundColor Yellow }
}
if (Test-Path "*.spec") { 
    try { Remove-Item -Path "*.spec" -Force -ErrorAction Stop }
    catch { Write-Host "Não foi possível remover os arquivos .spec. Continuando..." -ForegroundColor Yellow }
}

# Gerar executável
Write-Host "Gerando executável..." -ForegroundColor Yellow
python -m PyInstaller --onefile --windowed --name "Schema Colector" schema_colector_gui.py

# Desativar ambiente virtual
deactivate

Write-Host "`nBuild concluído com sucesso!" -ForegroundColor Green
Write-Host "O executável está disponível em: dist\Schema Colector.exe" -ForegroundColor Cyan

# Aguardar input do usuário
Write-Host "`nPressione qualquer tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 