# Gerenciamento de Coleta Seletiva ♻️

Este projeto é uma aplicação em Python para gerenciar resíduos recicláveis, cooperativas de coleta seletiva e agendamentos. Além disso, oferece relatórios visuais para análise da coleta seletiva.

## 📋 Funcionalidades

- **Cadastro de Resíduos**:
  - Tipos suportados: Plástico, Vidro, Metal e Papel.
  - Registra a quantidade e a data automaticamente.
- **Cadastro de Cooperativas**:
  - Armazena nome e endereço das cooperativas.
- **Agendamento de Coletas**:
  - Permite agendar coletas para cooperativas cadastradas em datas específicas.
- **Geração de Relatórios**:
  - Gráficos de barras exibem os tipos e as quantidades de resíduos registrados.

## 🛠️ Tecnologias Utilizadas

- **Python**:
  - Linguagem principal do projeto.
- **Tkinter**:
  - Biblioteca para criação da interface gráfica.
- **tkcalendar**:
  - Biblioteca para seleção de datas em um calendário.
- **Matplotlib**:
  - Biblioteca para geração de gráficos.
- **Datetime**:
  - Manipulação de datas e horários.

## 📊 Geração de Relatórios

A funcionalidade de geração de relatórios permite que os dados dos resíduos registrados sejam visualizados em um gráfico de barras, facilitando o acompanhamento e a análise do volume de resíduos. 

- **Como Funciona**:
  - O sistema agrupa os resíduos cadastrados por tipo (Plástico, Vidro, Metal e Papel).
  - Calcula automaticamente a quantidade total de cada tipo.
  - Exibe um gráfico de barras com:
    - **Eixo X**: Tipos de resíduos.
    - **Eixo Y**: Quantidade total registrada (em quilogramas).
    - **Barras Coloridas**: Representam visualmente os dados, com os valores exibidos acima de cada barra.

- **Exemplo de Relatório**:
  - **Entrada**:
    - Plástico: 50 kg.
    - Vidro: 20 kg.
    - Metal: 10 kg.
    - Papel: 15 kg.
  - **Saída**:
    - Um gráfico de barras com as seguintes informações:
      - Plástico: 50 kg.
      - Vidro: 20 kg.
      - Metal: 10 kg.
      - Papel: 15 kg.

- **Tratamento de Erros**:
  - Caso não haja resíduos registrados, o sistema exibe uma mensagem de erro: 
    - `"Não há resíduos registrados para gerar o relatório."`

