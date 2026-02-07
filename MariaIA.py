from datetime import datetime
import wikipedia
import random

# Configurar idioma da Wikipedia
wikipedia.set_lang("pt")

class MariaIA:
    def __init__(self):
        self.nome_usuario = None

    def buscar_wikipedia(self, termo):
        try:
            resumo = wikipedia.summary(termo, sentences=2)
            return resumo
        except wikipedia.exceptions.DisambiguationError as e:
            return f"O termo é ambíguo, pode se referir a: {', '.join(e.options[:5])}..."
        except wikipedia.exceptions.PageError:
            return "Não encontrei nada na Wikipedia sobre isso."

    def responder(self, pergunta):
        pergunta = pergunta.lower()

        if "meu nome é" in pergunta:
            self.nome_usuario = pergunta.replace("meu nome é", "").strip().capitalize()
            return f"Prazer em te conhecer, {self.nome_usuario}!"

        elif "qual é o meu nome" in pergunta:
            return f"Você me disse que seu nome é {self.nome_usuario}." if self.nome_usuario else "Ainda não sei seu nome. Diga 'meu nome é ...'."

        elif "oi" in pergunta or "olá" in pergunta:
            if self.nome_usuario:
                return random.choice([
                    f"Oi {self.nome_usuario}, como você está?",
                    f"Olá {self.nome_usuario}, tudo bem?",
                    f"E aí {self.nome_usuario}, beleza?",
                    f"Oi oi {self.nome_usuario}, pronto pra conversar?"
                ])
            else:
                return random.choice([
                    "Oi! Como você está?",
                    "Olá, tudo bem?",
                    "E aí, beleza?",
                    "Oi oi, pronto pra conversar?"
                ])

        elif "bem" in pergunta or "bem e voce?" in pergunta:
            return random.choice([
                "Eu estou ótimo!",
                "Estou bem também 😁",
                "Tudo tranquilo por aqui!",
                "Melhor agora falando com você!"
            ])

        elif "quem é você" in pergunta or "qual é o seu nome?" in pergunta or "como voce se chama?" in pergunta:
            return "Sou a Maria!"

        elif "quem é o seu criador" in pergunta or "quem te criou" in pergunta:
            return "O Sr. Rodrigo! O fodão!"

        elif "qual a sua linguagem favorita" in pergunta:
            return "Com certeza Python 🐍!"

        elif "que horas são" in pergunta or "me diga as horas" in pergunta or "hora" in pergunta:
            agora = datetime.now()
            hora = agora.strftime("%H:%M")

            dias_semana = {
                "Monday": "segunda-feira",
                "Tuesday": "terça-feira",
                "Wednesday": "quarta-feira",
                "Thursday": "quinta-feira",
                "Friday": "sexta-feira",
                "Saturday": "sábado",
                "Sunday": "domingo"
            }

            meses = {
                "01": "janeiro", "02": "fevereiro", "03": "março", "04": "abril",
                "05": "maio", "06": "junho", "07": "julho", "08": "agosto",
                "09": "setembro", "10": "outubro", "11": "novembro", "12": "dezembro"
            }

            dia_semana = dias_semana[agora.strftime("%A")]
            dia = agora.strftime("%d")
            mes = meses[agora.strftime("%m")]
            ano = agora.strftime("%Y")

            data_extenso = f"{dia} de {mes} de {ano}"
            return f"Agora são {hora} de {dia_semana}, {data_extenso}."

        elif "wikipedia" in pergunta:
            termo = pergunta.replace("wikipedia", "").strip()
            return self.buscar_wikipedia(termo) if termo else "Diga o que você quer pesquisar na Wikipedia."

        elif "adeus" in pergunta or "tchau" in pergunta:
            return random.choice([
                "Até logo! Foi bom conversar com você.",
                "Tchauzinho, até a próxima!",
                "Falou! Se cuida!",
                "Até mais!"
            ])

        else:
            return "Desculpe, ainda não aprendi a responder isso."


# Loop de chat
if __name__ == "__main__":
    maria = MariaIA()
    while True:
        pergunta = input("Digite: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Maria: Saindo... até mais!")
            break
        print("Maria:", maria.responder(pergunta))