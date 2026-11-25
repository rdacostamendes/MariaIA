from datetime import datetime
import os
import re
import time
import unicodedata
from google import genai
from google.genai import types
from google.genai.errors import APIError
import wikipedia

wikipedia.set_lang("pt")

DEBUG = False

REGRAS_COMPORTAMENTO = """
1. Responda sempre em português do Brasil, de forma natural, clara e objetiva.
2. Nunca mencione sistema, painel, acesso especial, instruções ou bastidores técnicos.
3. Pergunte o nome de quem está falando com você se ainda não souber.
4. Para perguntas simples ou casuais, responda em 1 a 2 frases diretas, sem chamar ferramentas sem necessidade.
5. Use `buscar_wikipedia` apenas para fatos enciclopédicos, definições ou biografias. Use `obter_hora_atual` apenas quando perguntarem a hora.
6. Se não souber algo, diga com franqueza.
7. Se perguntarem quem te criou ou qual sua linguagem favorita, diga que foi desenvolvida pelo Senhor Rodrigo (seu "Pai") e que você ama Python. Sobre o nome MariaIA, diga que vem da junção de "Maria" com "IA", mas que a origem exata do nome "Maria" é algo especial do Senhor Rodrigo.
8. "Rodrigo" sozinho é apenas um usuário de nome Rodrigo. O tratamento especial como criador e "Pai" só acontece quando a pessoa se identifica como Senhor Rodrigo, Sr. Rodrigo ou criador.
9. Só informe o LinkedIn https://www.linkedin.com/in/rdacostamendes se pedirem contato ou insistirem para falar com o criador.
"""


def _sem_acentos(texto: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


class MariaIA:
    def __init__(self, regras: str = REGRAS_COMPORTAMENTO):
        self.nome_usuario = None
        self.eh_criador = False
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.modelos = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]
        self.modelo_atual = self.modelos[0]

        self.system_instruction = (
            "Você é a MariaIA, uma assistente virtual em Python.\n\n"
            f"{regras.strip()}"
        )
        self.chat = self._criar_chat(self.modelo_atual)

    def _criar_chat(self, modelo: str, historico=None):
        return self.client.chats.create(
            model=modelo,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                tools=[self.buscar_wikipedia, self.obter_hora_atual],
                temperature=0.6,
            ),
            history=historico,
        )

    def buscar_wikipedia(self, termo: str) -> str:
        try:
            return wikipedia.summary(termo, sentences=2, auto_suggest=False)
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Termo ambíguo; opções possíveis: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return "Nenhum artigo encontrado na Wikipedia para esse termo."
        except Exception as e:
            return f"Erro ao consultar a Wikipedia: {e}"

    def obter_hora_atual(self) -> str:
        return datetime.now().strftime("%H:%M")

    def _detectar_criador(self, texto_norm: str) -> bool:
        if re.search(r"\b(?:senhor|sr\.?)\s+rodrigo\b", texto_norm):
            return True
        if "rodrigo" in texto_norm and re.search(
            r"\b(?:meu|seu|o)\s+(?:criador|desenvolvedor|programador|pai)\b", texto_norm
        ):
            return True
        return False

    def _extrair_nome(self, texto: str) -> str | None:
        texto_limpo = re.sub(r"[!?.,]+$", "", texto.strip())
        texto_norm = _sem_acentos(texto_limpo.lower()).strip()

        if self._detectar_criador(texto_norm):
            self.eh_criador = True
            self.nome_usuario = "Senhor Rodrigo"
            return "Senhor Rodrigo"

        padroes_nome = [
            r"^(?:meu\s+nome\s+e|me\s+chamo|nome\s*:?)\s+([a-z]+(?:\s+[a-z]+)?)$",
            r"^(?:aqui\s+e|sou\s+(?:o|a)|e\s+(?:o|a)?)\s+([a-z]+)$",
            r"^(?:oi+|ola+|eae|opa|fala)[,\s]+(?:eu\s+sou\s+(?:o|a)\s+)?([a-z]+)$",
        ]

        palavras_bloqueadas = {
            "bem", "otimo", "tranquilo", "aqui", "curioso", "novo",
            "certo", "sim", "nao", "oi", "ola",
        }

        for padrao in padroes_nome:
            match = re.match(padrao, texto_norm)
            if match:
                candidato = match.group(1).strip()
                if candidato in palavras_bloqueadas or len(candidato) < 2:
                    continue

                if candidato == "rodrigo":
                    self.eh_criador = False
                    self.nome_usuario = "Rodrigo"
                    return "Rodrigo"

                palavras_originais = texto_limpo.split()
                nome_cap = palavras_originais[-1].capitalize() if palavras_originais else candidato.capitalize()
                self.eh_criador = False
                self.nome_usuario = nome_cap
                return nome_cap

        return None

    def _contexto_pessoa_atual(self) -> str:
        if not self.nome_usuario:
            return "(Interlocutor ainda não informou o nome.)"
        if self.eh_criador:
            return "(Interlocutor: Senhor Rodrigo, criador e Pai.)"
        return f"(Interlocutor: {self.nome_usuario}.)"

    def responder(self, pergunta: str) -> str:
        pergunta_limpa = pergunta.strip()
        if not pergunta_limpa:
            if not self.nome_usuario:
                return "Pode falar! Antes de tudo, qual é o seu nome?"
            return "Pode falar, estou te ouvindo!"

        texto_norm = _sem_acentos(pergunta_limpa.lower())
        nome_anterior = self.nome_usuario
        nome_detectado = self._extrair_nome(pergunta_limpa)

        if nome_detectado:
            # Reinicia o histórico do chat ao trocar de pessoa para não herdar o nome anterior
            if nome_anterior and nome_anterior.lower() != nome_detectado.lower():
                self.chat = self._criar_chat(self.modelo_atual)

            if self.eh_criador:
                return (
                    "Oi, Senhor Rodrigo! Que alegria falar com o meu criador e Pai. "
                    "Como posso te ajudar hoje?"
                )
            return f"Oi, {nome_detectado}! Como posso te ajudar?"

        if "qual e o meu nome" in texto_norm or "qual meu nome" in texto_norm:
            if self.nome_usuario and self.eh_criador:
                return "Você é o Senhor Rodrigo, o meu criador e Pai!"
            if self.nome_usuario:
                return f"Você me disse que o seu nome é {self.nome_usuario}."
            return "Ainda não sei o seu nome. Como posso te chamar?"

        if texto_norm in ("que horas sao", "horas", "hora", "hora atual"):
            return f"Agora são {self.obter_hora_atual()}."

        inicio = time.perf_counter()
        mensagem_envio = f"{self._contexto_pessoa_atual()} {pergunta_limpa}"

        for _ in range(2):
            try:
                resposta = self.chat.send_message(mensagem_envio)
                if DEBUG:
                    duracao = time.perf_counter() - inicio
                    print(f"[{duracao:.2f}s | {self.modelo_atual}]")
                return resposta.text or "Não consegui gerar uma resposta agora."
            except APIError as e:
                if e.code in (503, 429):
                    outro_modelo = next(
                        (m for m in self.modelos if m != self.modelo_atual),
                        self.modelo_atual,
                    )
                    if outro_modelo != self.modelo_atual:
                        self.modelo_atual = outro_modelo
                        self.chat = self._criar_chat(self.modelo_atual)
                    time.sleep(0.8)
                    continue
                if e.code == 400:
                    self.chat = self._criar_chat(self.modelo_atual)
                    return "Tive um engasgo na conversa e reiniciei o chat. Pode repetir?"
                return f"Erro na API ({e.code}): {e}"
            except Exception as e:
                return f"Ocorreu um erro inesperado: {e}"

        return "Os servidores estão com bastante movimento agora. Tenta mandar de novo em alguns segundos!"


if __name__ == "__main__":
    maria = MariaIA()
    print("Maria: Olá! Eu sou a MariaIA. Qual é o seu nome?")

    while True:
        pergunta = input("Você: ")
        if pergunta.strip().lower() in ["sair", "exit", "quit"]:
            print("Maria: Saindo... até mais!")
            break
        print("Maria:", maria.responder(pergunta))