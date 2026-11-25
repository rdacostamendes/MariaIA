# MariaIA — Assistente Virtual em Python

Assistente virtual conversacional desenvolvida em **Python** com integração à **API do Google Gemini**, consulta rápida à **Wikipedia** e interface web interativa construída com **Flask**, **HTML5**, **CSS3** e **JavaScript**.

---

## Funcionalidades

- **Conversação natural com IA:** integração com a SDK `google-genai` utilizando modelos Gemini.
- **Interface web reativa:** orbe animado em `<canvas>` (inspirado no visual *Grande Sábio / Rafael*) que reage ao processamento e alterna automaticamente entre o tema **dourado** (visitantes) e **rosa** (modo criador).
- **Efeito de digitação e links clicáveis:** respostas exibidas progressivamente com conversão automática de URLs em links externos.
- **Controle de identificação de usuário:** diferencia visitantes comuns (incluindo usuários chamados *Rodrigo*) do criador (*Senhor Rodrigo / Sr. Rodrigo*), mantendo o contexto da sessão e permitindo reiniciar a conversa a qualquer momento.
- **Ferramentas integradas:**
  - Busca de resumos enciclopédicos na Wikipedia em português (`wikipedia`).
  - Consulta de horário local atual.

---

## Estrutura do Projeto

```text
MariaIA/
├── MariaIA.py          # Núcleo lógico da assistente, regras de comportamento e integração com Gemini
├── app.py              # Servidor Flask e rotas REST (/chat e /reset)
├── templates/
│   └── index.html      # Interface web completa (orbe de partículas, chat e temas dinâmicos)
├── .gitignore          # Arquivos e diretórios locais ignorados no versionamento
└── README.md           # Documentação do projeto