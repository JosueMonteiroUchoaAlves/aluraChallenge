from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button
from textual.containers import Container, Vertical
import google.generativeai as genai
import asyncio

# Configurar API do Gemini (substitua pela sua chave)
genai.configure(api_key="AIzaSyANuWDVQs8CHuSfnpOY0mZYYrBrW3bECHQ")

NGO_DATA = {
    "São Paulo": [
        {"nome": "Fundo Água São Paulo", "distancia": "5km", "contato": "contato@spagua.org", "missao": "Acesso à água potável"},
        {"nome": "Comida para Todos SP", "distancia": "3km", "contato": "info@comidaparatodos.org", "missao": "Combater a fome"}
    ],
    "Rio de Janeiro": [
        {"nome": "Rios Limpos RJ", "distancia": "4km", "contato": "info@rioslimpos.org", "missao": "Limpeza de rios"},
        {"nome": "EducaRio", "distancia": "6km", "contato": "contato@educario.org", "missao": "Acesso à educação"}
    ]
}

def gerar_modelo():
    return genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

def prompt_model(model, prompt):
    return model.generate_content(prompt).text

def estruturar_plano(p, o, t, l):
    prompt = f"""
    Você é um Mentor de Impacto Social por IA. Restruture as entradas do usuário em um resumo de plano claro e conciso em markdown.
    **Entrada:**
    - Problema: {p}
    - Orçamento: {o}
    - Tempo: {t}
    - Local: {l}
    """
    try:
        return prompt_model(gerar_modelo(), prompt)
    except Exception as e:
        return f"### Resumo do Plano\nErro: {str(e)}"

def dividir_tarefas(p, o, t, l):
    prompt = f"""
    Divida o plano em 4–6 passos acionáveis. Markdown em português.
    - Problema: {p}
    - Orçamento: {o}
    - Tempo: {t}
    - Local: {l}
    """
    try:
        return prompt_model(gerar_modelo(), prompt)
    except Exception as e:
        return f"### Plano de Ação\nErro: {str(e)}"

def estimar_custos(p, o):
    prompt = f"""
    Estime custos para o problema '{p}' com orçamento de R${o}. Liste itens com preços. Saída em markdown.
    """
    try:
        return prompt_model(gerar_modelo(), prompt)
    except Exception as e:
        return f"### Estimativa de Custos\nErro: {str(e)}"

def buscar_ongs(p, l):
    prompt = f"""
    Sugira 2 ONGs em {l} para o problema '{p}', com nome, distância, contato e missão. Saída em markdown.
    """
    try:
        return prompt_model(gerar_modelo(), prompt)
    except Exception:
        fallback = NGO_DATA.get(l, [
            {"nome": "ONG Genérica 1", "distancia": "Desconhecida", "contato": "contato@ong1.org", "missao": "Apoio geral"},
            {"nome": "ONG Genérica 2", "distancia": "Desconhecida", "contato": "contato@ong2.org", "missao": "Apoio geral"}
        ])
        return "\n".join([
            "### ONGs Sugeridas",
            *[f"- **{ong['nome']}**: {ong['distancia']}, contato: {ong['contato']}, missão: {ong['missao']}" for ong in fallback]
        ])

def gerar_motivacao(p, l, progresso):
    motivacoes = {
        "inicial": "Incentive o usuário a começar sua jornada com confiança.",
        "em andamento": "Celebre o progresso e sugira próximos passos.",
        "travado": "Empatize com a frustração e ofereça ajuda." 
    }
    prompt = f"""
    Gere uma mensagem motivacional sobre {p} em {l}. Progresso: {motivacoes.get(progresso, 'Incentive de forma geral')}. Markdown.
    """
    try:
        return prompt_model(gerar_modelo(), prompt)
    except Exception as e:
        return f"### Mensagem Motivacional\nErro: {str(e)}"

class MentorApp(App):
    CSS_PATH = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            with Vertical():
                yield Input(placeholder="Problema social", id="problema")
                yield Input(placeholder="Orçamento (R$)", id="orcamento")
                yield Input(placeholder="Tempo disponível (h)", id="tempo")
                yield Input(placeholder="Local", id="local")
                yield Input(placeholder="Progresso (inicial/em andamento/travado)", id="progresso")
                yield Button("Gerar Plano", id="gerar")
                yield Static("", id="output")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "gerar":
            asyncio.create_task(self.gerar_resposta())

    async def gerar_resposta(self):
        p = self.query_one("#problema", Input).value
        o = self.query_one("#orcamento", Input).value
        t = self.query_one("#tempo", Input).value
        l = self.query_one("#local", Input).value
        progresso = self.query_one("#progresso", Input).value or "inicial"

        if not all([p, o, t, l]):
            self.query_one("#output", Static).update("[b]Erro:[/b] Todos os campos são obrigatórios.")
            return

        output = "\n\n".join([
            estruturar_plano(p, o, t, l),
            dividir_tarefas(p, o, t, l),
            estimar_custos(p, o),
            buscar_ongs(p, l),
            gerar_motivacao(p, l, progresso)
        ])

        self.query_one("#output", Static).update(output)

if __name__ == "__main__":
    MentorApp().run()
