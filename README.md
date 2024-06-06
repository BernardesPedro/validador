# Validador de Ambiente

## Descrição

O Validador de Ambiente é uma ferramenta desenvolvida em Python para verificar a configuração de hardware e software de um sistema Linux. O script valida informações do processador, memória, sistema operacional, disco, velocidade da internet e acessibilidade de portas internas e externas.

## Funcionalidades

- **Processador**: Modelo, quantidade de núcleos, arquitetura e velocidade.
- **Memória**: Total de RAM e SWAP.
- **Sistema Operacional**: Nome, distribuição, versão e arquitetura.
- **Disco**: Tamanho total da partição raiz e percentual de uso.
- **Internet**: Velocidade de download, upload e ping.
- **Portas**: Verificação de acessibilidade interna e externa para as portas especificadas.

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python:
  - psutil
  - speedtest-cli
  - distro
  - colorama
  - tqdm
  - requests

## Instalação

1. Clone o repositório:

    ```sh
    git clone https://github.com/BernardesPedro/validador.git
    cd validador-ambiente
    ```

2. Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

3. Execute o script:

    ```sh
    python validador.py
    ```

## Geração de Binário Único

Para gerar um binário único usando PyInstaller, siga os passos abaixo:

1. Instale o PyInstaller:

    ```sh
    pip install pyinstaller
    ```

2. Gere o binário:

    ```sh
    pyinstaller --onefile --noconsole validador.py
    ```

3. O binário gerado estará na pasta `dist`.

## Problemas Conhecidos

- Em sistemas mais antigos, pode ocorrer o erro relacionado à versão do `GLIBC`. Para resolver isso, recomenda-se construir o binário em um ambiente com uma versão mais antiga do `GLIBC`, como CentOS 7. 

## Uso do Docker para Construção

Uma maneira prática de garantir a compatibilidade com versões mais antigas do `GLIBC` é usar Docker. Aqui está um exemplo de como fazer isso:

1. Crie um `Dockerfile`:

    ```dockerfile
    FROM centos:7

    # Instale as dependências necessárias
    RUN yum -y update && \
        yum -y install epel-release && \
        yum -y install python3 python3-pip python3-devel gcc make glibc-static

    # Copie o seu código para o contêiner
    WORKDIR /app
    COPY . /app

    # Instale as dependências do Python
    RUN pip3 install --upgrade pip
    RUN pip3 install pyinstaller psutil speedtest-cli distro colorama tqdm requests

    # Construa o binário com PyInstaller
    RUN pyinstaller --onefile --noconsole validador.py

    # Defina o ponto de entrada padrão para o contêiner
    ENTRYPOINT ["/app/dist/validador"]
    ```

2. Construa a imagem Docker:

    ```sh
    docker build -t validador-builder .
    ```

3. Execute o contêiner para obter o binário:

    ```sh
    docker run --rm -v $(pwd)/dist:/app/dist validador-builder
    ```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.


---
