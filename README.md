# Tic Tac AI

Projeto em desenvolvimento que combina um jogo da velha jogável no navegador com uma API em Python para registrar partidas, avaliar jogadas e preparar a base para um agente de aprendizado por reforço.

Atualmente, o jogador humano joga com `X` e o agente joga com `O`. A API controla o fluxo da partida, valida estados de vitória ou empate, registra as jogadas em SQLite e atribui recompensas iniciais para futuras etapas de treinamento.

## Objetivo

Criar um agente capaz de aprender a jogar jogo da velha a partir das partidas registradas, evoluindo de escolhas aleatórias para uma estratégia treinada por reforço.

## Stack

- Python
- FastAPI
- SQLModel
- SQLite
- HTML, CSS e JavaScript

## O que já existe

- Interface simples para jogar no navegador
- Backend com rotas para criar partidas e registrar jogadas
- Persistência de partidas e movimentos em banco SQLite
- Verificação de vitória, empate e casas disponíveis
- Sistema inicial de recompensas para avaliar jogadas do agente
- Agente inicial com escolha aleatória entre movimentos válidos

## Próximos passos

- Treinar o modelo para jogar de forma estratégica
- Usar o histórico de partidas e recompensas como base de aprendizado
- Melhorar a função de recompensa
- Comparar desempenho entre agente aleatório e agente treinado
- Evoluir a interface para exibir placar, histórico e status do modelo

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Inicie a API:

```bash
uvicorn main:app --reload
```

Acesse:

```text
http://127.0.0.1:8000
```

## Status

Este projeto ainda não está completo. A estrutura principal do jogo e da API já foi criada, e a próxima etapa é implementar o treinamento do modelo para que o agente aprenda a jogar melhor ao longo do tempo.
