from datetime import datetime
import wikipedia
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configurar idioma da Wikipedia
wikipedia.set_lang("pt")

class MariaIA:
    def __init__(self):
        self.nome_usuario = None
        
        # 1. BASE DE CONHECIMENTO (Exemplos para treinar a IA)
        # Quanto mais frases de exemplo você colocar aqui, mais inteligente a Maria fica!
        self.treinamento = {
            "saudacao": [
                "oi", "olá", "ola", "eae", "opa", "bom dia", "boa tarde", "boa noite",
                "olá maria", "oi tudo bem", "como vai", "fala ai", "salve"
            ],
            "estado_usuario": [
                "estou bem", "to bem", "tudo bem por aqui", "tudo ótimo", "estou tranquilo",
                "bem e voce", "tudo bem e com voce", "to otimo", "tudo certinho"
            ],
            "nome_ia": [
                "qual o seu nome", "quem é você", "como voce se chama", "seu nome",
                "quem fala", "qual seu nome"
            ],
            "criador": [
                "quem te criou", "quem é seu criador", "quem te desenvolveu", "quem fez voce",
                "quem é seu programador", "quem foi o foda que te programou", "seu pai"
            ],
            "linguagem_favorita": [
                "qual a sua linguagem favorita", "qual linguagem voce prefere", 
                "voce gosta de python", "qual sua tecnologia favorita", "linguagem preferida"
            ],
            "despedida": [
                "adeus", "tchau", "fui", "ate logo", "até mais", "vou nessa", "abraço"
            ]
        }
        
        # Respostas possíveis para cada intenção
        self.respostas = {
            "saudacao": [
                "Oi! Como você está?", "Olá, tudo bem?", "E aí, beleza?", "Oi oi, pronto pra conversar?"
            ],
            "estado_usuario": [
                "Eu estou ótima!", "Estou bem também 😁", "Tudo tranquilo por aqui!", "Melhor agora falando com você!"
            ],
            "nome_ia": [
                "Sou a Maria!", "Me chamo Maria, sua assistente virtual em Python."
            ],
            "criador": [
                "O Sr. Rodrigo! O fodão!", "Fui desenvolvida pelo mestre Rodrigo!"
            ],
            "linguagem_favorita": [
                "Com certeza Python 🐍!", "Eu amo Python, mas sei que meu criador anda codando em C na faculdade... 👀"
            ],
            "despedida": [
                "Até logo! Foi bom conversar com você.", "Tchauzinho, até a próxima!", "Falou! Se cuida!", "Até mais!"
            ]
        }
        
        # 2. TREINAR O MODELO DE ML
        self.frases_treino = []
        self.classes_treino = []
        
        # Desmembra o dicionário em duas listas alinhadas (frases e suas respectivas classes)
        for classe, frases in self.treinamento.items():
            for frase in frases:
                self.frases_treino.append(frase.lower())
                self.classes_treino.append(classe)
                
        # O Vectorizer converte os textos em uma matriz de números (pesos matemáticos)
        self.vectorizer = TfidfVectorizer()
        self.X_treino = self.vectorizer.fit_transform(self.frases_treino)

    def buscar_wikipedia(self, termo):
        try:
            return wikipedia.summary(termo, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            return f"O termo é ambíguo, pode se referir a: {', '.join(e.options[:5])}..."
        except wikipedia.exceptions.PageError:
            return "Não encontrei nada na Wikipedia sobre isso."

    def responder(self, pergunta):
        pergunta_limpa = pergunta.lower().strip()

        # --- REGRAS ESPECÍFICAS (Ainda necessárias para capturar variáveis ou comandos externos) ---
        if "meu nome é" in pergunta_limpa:
            self.nome_usuario = pergunta.replace("meu nome é", "").strip().capitalize()
            return f"Prazer em te conhecer, {self.nome_usuario}!"

        if "qual é o meu nome" in pergunta_limpa:
            return f"Você me disse que seu nome é {self.nome_usuario}." if self.nome_usuario else "Ainda não sei seu nome. Diga 'meu nome é ...'."

        if "wikipedia" in pergunta_limpa:
            termo = pergunta_limpa.replace("wikipedia", "").strip()
            return self.buscar_wikipedia(termo) if termo else "Diga o que você quer pesquisar na Wikipedia."

        if any(w in pergunta_limpa for w in ("horas", "hora", "que horas")):
            agora = datetime.now()
            hora = agora.strftime("%H:%M")
            return f"Agora são {hora}."

        # --- PROCESSO DE MACHINE LEARNING ---
        # 1. Transforma a pergunta do usuário nos mesmos parâmetros numéricos do treino
        vetor_pergunta = self.vectorizer.transform([pergunta_limpa])
        
        # 2. Calcula a similaridade de cosseno (o quão perto a pergunta está de cada frase de treino)
        similaridades = cosine_similarity(vetor_pergunta, self.X_treino)
        
        # 3. Pega o índice da frase que teve a maior nota de proximidade
        melhor_match_idx = list(similaridades[0]).index(max(similaridades[0]))
        nota_confianca = similaridades[0][melhor_match_idx]
        
        # Se a IA tiver pelo menos 25% de certeza da intenção, ela responde
        if nota_confianca > 0.25:
            classe_predita = self.classes_treino[melhor_match_idx]
            resposta = random.choice(self.respostas[classe_predita])
            
            # Personalização com o nome do usuário se ele já tiver se identificado
            if self.nome_usuario and classe_predita == "saudacao":
                resposta = resposta.replace("!", f" {self.nome_usuario}!")
                
            return resposta
        
        return "Desculpe, ainda não aprendi a responder isso com clareza."

# Loop de chat
if __name__ == "__main__":
    maria = MariaIA()
    print("Maria: Olá! Eu sou Maria. Vamos conversar?")
    
    while True:
        pergunta = input("Você: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Maria: Saindo... até mais!")
            break
        print("Maria:", maria.responder(pergunta))