# Tic Tac AI

O **Tic Tac AI** é um jogo da velha no qual uma pessoa enfrenta um agente que melhora suas escolhas com base nas recompensas e no histórico das partidas já disputadas. O jogador humano usa **X**, enquanto o agente usa **O**.

O projeto reúne uma API em Python, responsável pelas regras e pela tomada de decisão, e uma interface web desenvolvida com Next.js. Cada partida e cada jogada são armazenadas em um banco SQLite, permitindo que experiências anteriores influenciem as próximas escolhas do agente.

> O agente ainda não utiliza uma rede neural nem um treinamento tradicional. Seu comportamento atual é um método simples de aprendizado por recompensa, apoiado pelo histórico salvo no banco de dados.

## Como o projeto funciona

Ao abrir a aplicação, o frontend solicita à API a criação de uma nova partida. Depois disso, o fluxo acontece da seguinte maneira:

1. A pessoa escolhe uma casa livre no tabuleiro e joga com **X**.
2. O frontend envia a posição escolhida para a API.
3. A API registra a jogada e verifica se houve vitória ou empate.
4. Se a partida continuar, o agente avalia as casas disponíveis e escolhe onde jogar com **O**.
5. A jogada do agente recebe uma recompensa, é salva no banco e retorna ao frontend.
6. O tabuleiro é atualizado e, quando a partida termina, a interface informa o vencedor ou o empate.

## Como o agente escolhe uma jogada

A escolha não é simplesmente aleatória. O agente monta uma matriz de pesos para as nove casas do tabuleiro e transforma esses pesos em probabilidades. Casas ocupadas recebem peso zero, portanto não podem ser selecionadas.

Para cada casa livre, o agente procura partidas anteriores que começaram com a mesma sequência de jogadas da partida atual. Quando encontra situações semelhantes, ele consulta as recompensas obtidas após a escolha daquela casa e usa a média desses resultados como peso. Se ainda não houver histórico útil, a casa recebe o peso inicial de `0,15`.

Depois, todos os pesos são normalizados, fazendo com que a soma seja igual a `1`. A jogada é sorteada com essas probabilidades: uma casa com recompensa histórica maior tem mais chance de ser escolhida, mas o agente ainda pode explorar outras opções.

Em resumo:

```text
estado atual do tabuleiro
          ↓
busca por partidas anteriores semelhantes
          ↓
média das recompensas de cada casa disponível
          ↓
conversão dos pesos em probabilidades
          ↓
escolha da próxima jogada do agente
```

### Recompensas simples

Antes de salvar a jogada do agente, a API calcula uma recompensa imediata:

- **+0,15** para cada linha, coluna ou diagonal em que a jogada bloqueia dois **X**;
- **+0,30** para cada linha, coluna ou diagonal aberta que já contém um **O**, incentivando a continuidade de uma formação;
- **+1,00** quando a jogada resulta na vitória do agente.

Se a pessoa vencer, a última jogada do agente tem sua recompensa zerada. Esses valores ficam registrados e ajudam a orientar decisões futuras em estados semelhantes.

## Tecnologias utilizadas

### Backend

- Python;
- FastAPI;
- SQLModel e SQLAlchemy;
- NumPy;
- SQLite.

### Frontend

- Next.js 16;
- React 19;
- TypeScript;
- Tailwind CSS 4.

## Estrutura principal

```text
tic_tac_ai/
├── main.py                  # API, fluxo da partida e verificação do resultado
├── db.py                    # Modelos e conexão com o banco SQLite
├── rl/
│   ├── agent.py             # Avaliação do histórico e escolha probabilística
│   └── enviroment.py        # Cálculo das recompensas imediatas
├── requirements.txt         # Dependências do backend
└── frontend/
    ├── app/                 # Páginas, componentes e integração com a API
    └── package.json         # Dependências e comandos do frontend
```

## Como executar

Você precisará ter o **Python** e o **Node.js** instalados. O backend e o frontend devem ser executados ao mesmo tempo, em terminais separados.

### 1. Inicie o backend

Na raiz do projeto, crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows, a ativação pode ser feita com:

```powershell
.venv\Scripts\activate
```

Instale as dependências e inicie a API:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

A API ficará disponível em `http://localhost:8000`. O arquivo `db.sqlite` será criado automaticamente na primeira execução.

### 2. Inicie o frontend

Em outro terminal, acesse a pasta do frontend, instale as dependências e execute o servidor de desenvolvimento:

```bash
cd frontend
npm install
npm run dev
```

Agora é só abrir `http://localhost:3000` no navegador e jogar. Boa partida! 🎮

## Rotas da API

- `GET /`: cria uma partida e retorna seu identificador;
- `POST /play`: recebe o identificador da partida, a linha e a coluna escolhidas pela pessoa; registra a rodada e, se possível, retorna a jogada do agente.

## Status do projeto

O fluxo principal já está funcionando: é possível criar uma partida, jogar pela interface, registrar os movimentos, detectar vitória ou empate e usar recompensas anteriores nas escolhas do agente.
