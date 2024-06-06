#!/bin/bash

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sem cor

# Função para exibir uma barra de progresso
progress_bar() {
  local duration=${1}
  local columns=$(tput cols)
  let _progress=(${duration}*${columns})/100
  let _done=(${_progress}*4)/10
  let _left=(${columns}-${_done})
  fill=$(printf "%${_done}s")
  empty=$(printf "%${_left}s")
  printf "\r${GREEN}[${fill// /#}${empty// /-}]${NC}"
}

# Verifica se o script está sendo executado como root
if [ "$(id -u)" -ne 0 ]; then
  echo -e "${RED}Este script deve ser executado como root${NC}"
  exit 1
fi

# Verifica a distribuição e versão do sistema operacional
echo -e "${CYAN}Verificando distribuição e versão do sistema operacional...${NC}"
. /etc/os-release

if [ "$ID" != "ubuntu" ] && [ "$ID" != "debian" ]; then
  echo -e "${RED}Distribuição não compatível. Apenas Ubuntu ou Debian são suportados.${NC}"
  echo -e "${YELLOW}Distribuição atual: $ID${NC}"
  exit 1
fi

if [ "$ID" == "ubuntu" ]; then
  required_version="22.04"
elif [ "$ID" == "debian" ]; then
  required_version="12"
fi

if [ "$(printf '%s\n' "$required_version" "$VERSION_ID" | sort -V | head -n1)" != "$required_version" ]; then
  echo -e "${RED}Versão do sistema não compatível. ${NC}"
  echo -e "${YELLOW}Versão atual: $VERSION_ID${NC}"
  echo -e "${YELLOW}É necessária a versão $required_version ou superior.${NC}"
  exit 1
fi

# Verifica a versão do GLIBC
echo -e "${CYAN}Verificando versão da GLIBC...${NC}"
required_glibc_version="2.35"
current_glibc_version=$(ldd --version | head -n 1 | awk '{print $NF}')

if [ "$(printf '%s\n' "$required_glibc_version" "$current_glibc_version" | sort -V | head -n1)" != "$required_glibc_version" ]; then
  echo -e "${RED}GLIBC versão $required_glibc_version ou superior é necessária.${NC}"
  echo -e "${YELLOW}Versão atual da GLIBC: $current_glibc_version${NC}"
  echo -e "${YELLOW}Versão do sistema:${NC}"
  cat /etc/os-release
  exit 1
fi
#echo -e "${CYAN}===============================${NC}"
#echo -e "${CYAN} Iniciando o processo de download e instalação ${NC}"
#echo -e "${CYAN}===============================${NC}"

# Define o URL de download e o caminho do executável
URL="http://go.maximasist.com.br/validador/validador"
DESTINO="/usr/local/bin/validador"

echo -e "${YELLOW}Download do validador...${NC}"
# Faz o download do arquivo com barra de progresso
curl -# -o "$DESTINO" "$URL" | while IFS= read -r -d '' c; do
  progress_bar $(( ${#c} * 100 / 8192 ))
done

if [ $? -ne 0 ]; then
  echo -e "${RED}Erro no download do arquivo${NC}"
  exit 1
fi

echo -e "\n${YELLOW}Dando permissão de execução ao arquivo...${NC}"
# Dá permissão de execução ao arquivo
chmod +x "$DESTINO"

echo -e "${YELLOW}Executando o arquivo validador...${NC}"
# Executa o arquivo
"$DESTINO"

if [ $? -eq 0 ]; then
  echo -e "${GREEN}Processo concluído!${NC}"
else
  echo -e "${RED}Ocorreu um erro durante a execução do validador${NC}"
fi
