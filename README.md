# POODev
[Documentação Oficial](https://drive.google.com/file/d/198d8ALFhHtB472u4Z-LPIPnCh2mRa6u2/view?usp=sharing)

**Matéria da UENF: Programação Orientada a Objetos e Desenvolvimento** 


Este repositório contém um sistema para geração de relatórios a partir de arquivos CSV, desenvolvido como parte da matéria de **Programação Orientada a Objetos e Desenvolvimento** da **Universidade Estadual do Norte Fluminense (UENF)**.

O sistema permite aos usuários carregar arquivos CSV, processar os dados e gerar relatórios em PDF. Esses relatórios podem ser baixados ou visualizados na interface do usuário, que também mostra o status dos relatórios gerados e em andamento.

## Visão Geral do Sistema

Este sistema foi projetado para facilitar a análise de dados CSV e transformar essas informações em relatórios fáceis de entender. Algumas características importantes do sistema incluem:

- **Upload de Arquivos CSV**: Os usuários podem enviar arquivos CSV para serem analisados.
- **Geração de Relatórios em PDF**: Os dados são processados, gerando relatórios em formato PDF com gráficos e insights.
- **Visualização dos Relatórios**: Uma página dedicada ("Meus Relatórios") onde os usuários podem visualizar e baixar todos os relatórios que foram gerados até o momento.
- **Tarefas Assíncronas com Redis e RQ**: A geração dos relatórios é feita de forma assíncrona, permitindo que o processo seja realizado em segundo plano.

### Tecnologias Utilizadas

- **Python (Flask)**: Para construção da aplicação web.
- **Redis**: Utilizado como um sistema de filas para gerenciar tarefas assíncronas.
- **RQ (Redis Queue)**: Utilizado para enfileirar e executar tarefas em segundo plano.
- **Pandas e Matplotlib**: Utilizados para análise e visualização dos dados do CSV.
- **FPDF**: Utilizado para gerar relatórios em PDF.

## Como Iniciar o Projeto

Para executar este sistema, siga os passos abaixo:

### Pré-requisitos

- **Python 3.8+**: Certifique-se de que Python está instalado. Você pode verificar usando:
  ```sh
  python --version
- **Pipenv ou Pip**: Utilizado para instalar as dependências necessárias.
- **Redis**: Redis deve estar instalado e funcionando. É utilizado para gerenciar as filas de tarefas.

### Passos para Iniciar o Sistema

1. **Clone o Repositório**

   Primeiro, clone este repositório para sua máquina local:

   ```sh
   git clone https://github.com/seu-usuario/POODev.git
   cd POODev
2. **Instale as Dependências**

    Utilize pip ou pipenv para instalar as dependências necessárias:

    ```sh
    pip install -r requirements.txt
3. **Inicie o Redis Server**

    O Redis precisa estar rodando para gerenciar as filas de tarefas do sistema. Para iniciar o Redis Server, use o comando:

    ```sh
    redis-server
4. **Inicie o Worker do RQ**

    Um worker do RQ é necessário para processar as tarefas de geração de relatório. Abra um novo terminal no diretório do projeto e execute:

    ```sh
    rq worker fila
5. **Inicie a Aplicação Flask**

    Finalmente, inicie a aplicação Flask. Abra outro terminal no diretório do projeto e execute:

    ```sh
    python app.py