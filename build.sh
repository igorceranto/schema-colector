#!/bin/bash
set -e

# Nome do executável e release
APP_NAME="schema_collector_gui"
RELEASE_DIR="release"
DIST_DIR="dist"
ZIP_NAME="${APP_NAME}_linux_$(date +%Y%m%d_%H%M%S).zip"

# Mensagens coloridas
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Iniciando processo de build...${NC}"

# Criar ambiente virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Criando ambiente virtual...${NC}"
    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar pip
echo -e "${YELLOW}Atualizando pip...${NC}"
pip install --upgrade pip

# Instalar dependências
echo -e "${YELLOW}Instalando dependências...${NC}"
pip install -r requirements.txt
pip install pyinstaller

# Limpar builds anteriores
echo -e "${YELLOW}Limpando builds anteriores...${NC}"
rm -rf build "$DIST_DIR" *.spec "$RELEASE_DIR"

# Gerar executável
echo -e "${YELLOW}Gerando executável...${NC}"
pyinstaller --onefile --windowed --name "$APP_NAME" schema_collector_gui.py

# Criar pasta de release e compactar
mkdir -p "$RELEASE_DIR"
cd "$DIST_DIR"
zip "../$RELEASE_DIR/$ZIP_NAME" "$APP_NAME"
cd ..

echo -e "${GREEN}Build concluído com sucesso!${NC}"
echo -e "Arquivo compactado disponível em: $RELEASE_DIR/$ZIP_NAME"

deactivate 