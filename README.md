# Maria IA 🧠🐍

A **Maria IA** é uma assistente virtual inteligente desenvolvida em Python. O projeto nasceu de uma motivação muito especial: homenagear a minha primeira filha, **Maria Helena**, unindo o início da minha jornada na tecnologia (ADS) com o momento mais importante da minha vida pessoal.

Diferente de chatbots comuns baseados apenas em regras rígidas (`if/else`), a Maria IA utiliza **Machine Learning (Aprendizado de Máquina)** para compreender o contexto e a intenção das frases do usuário, sendo capaz de deduzir respostas mesmo para perguntas que não foram explicitamente programadas.

---

## 🚀 Funcionalidades

* **Processamento de Linguagem Natural (PLN):** Identificação de intenções através de cálculo de proximidade semântica.
* **Respostas Dinâmicas:** Sorteio de variações de diálogos para tornar a conversação mais natural e menos repetitiva.
* **Integração com a Wikipedia:** Capacidade de buscar resumos de termos e conceitos em tempo real diretamente na plataforma.
* **Módulo de Tempo Real:** Consulta de data e hora do sistema atualizadas.
* **Memória de Contexto:** Capacidade de memorizar e resgatar o nome do usuário durante a sessão de chat.

---

## 🛠️ Stack Técnica e Conceitos de IA

Este projeto aplica conceitos fundamentais de Ciência de Dados e Inteligência Artificial no mundo real:

* **`scikit-learn`:** Utilização da biblioteca líder de mercado para estruturação do modelo preditivo.
* **TF-IDF Vectorization (`TfidfVectorizer`):** Algoritmo que transforma os textos digitados pelo usuário em vetores numéricos, calculando a relevância de cada palavra com base na frequência.
* **Similaridade de Cosseno (`cosine_similarity`):** Aplicação de cálculo matemático vetorial para medir a proximidade entre a pergunta feita no terminal e a base de conhecimento de treino da IA.
* **Orientação a Objetos (POO):** Toda a estrutura da IA encapsulada em uma classe organizada, facilitando a manutenção e a expansão de novas intenções.

---

## 📋 Exemplo de Inteligência (Dedução Baseada em IA)

Se a base de dados possui o exemplo de treino: *"Quem te criou?"* E o usuário digita no terminal: *"Quem foi o programador foda que te desenvolveu?"*

A **Maria IA** não quebra e nem responde que não entendeu. O modelo matemático calcula os pesos das palavras, identifica que a intenção se refere ao **Criador** e responde com sucesso:

```text
Você: Quem foi o programador foda que te desenvolveu?
Maria: O Sr. Rodrigo! O fodão!