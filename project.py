from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button, LoadingIndicator, Markdown
from textual.containers import Container, Vertical, Horizontal
from google import genai
import asyncio
import os

# Criar o cliente Gemini (usará a variável de ambiente GOOGLE_API_KEY automaticamente)
try:
    client = genai.Client(api_key='AIzaSyBA-onQsoRPtt4DXR-r6mmmoy5ZhKy3d_o')
except Exception as e:
    print(f"ERRO ao inicializar o cliente Google AI: {e}")
    print("Verifique sua GOOGLE_API_KEY e sua conexão de internet.")
    exit()

model_name = "gemini-2.5-flash-preview-04-17"

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
   
# Função fazer_pergunta modificada para usar o cliente e o nome do modelo
# Adicione no início do arquivo se ainda não tiver:
import traceback # Para imprimir o traceback completo em caso de erro

# ... (restante do seu código) ...

# Função fazer_pergunta modificada para usar o cliente e o nome do modelo
async def fazer_pergunta(prompt):
    """Faz uma chamada assíncrona à API do Gemini usando o cliente."""
    print(f"Chamando API com prompt (primeiras 500 chars): {prompt[:500]}...") # Depuração: Mostra o prompt
    try:
        # Usando o método generate_content através do cliente
        response = await asyncio.wait_for(
            asyncio.to_thread(
                client.models.generate_content,
                model=model_name, # Passa o nome do modelo aqui
                contents=prompt,
                # Opcional: Configurar para garantir saída markdown - descomente se precisar
                # generation_config={"response_mime_type": "text/markdown"}
            ),
            timeout=20.0 # Grande o timeout, pois as chamadas podem demorar um pouco
        )

        # Depuração: Mostra o objeto de resposta completo se não tiver texto ou for vazio
        if not hasattr(response, 'text') or not response.text:
             print(f"Aviso: Resposta da API sem texto válido ou vazia.")
             print(f"Objeto de resposta completo: {response}") # <-- IMPRIME O OBJETO COMPLETO AQUI
             return "**Erro:** Resposta da API sem texto válido ou vazia."

        # Depuração: Mostra o texto da resposta (primeiras 500 chars) se for bem-sucedida
        print(f"API retornou texto (primeiras 500 chars): {response.text[:500]}...")
        return response.text # Retorna o texto se tudo ok

    except asyncio.TimeoutError:
        print("Erro: Tempo limite excedido na chamada da API.") # Depuração: Confirma timeout
        return "**Erro:** Tempo limite da chamada à API excedido."
    except Exception as e:
        print(f"Erro na chamada da API: {e}") # Depuração: Imprime o erro capturado
        traceback.print_exc() # Depuração: Imprime o traceback completo do erro
        # Possível causa do problema: str(e) contém "{'@type':".
        # Para evitar isso, podemos retornar apenas uma mensagem genérica ou inspecionar 'e'
        # Mas por enquanto, vamos ver o que 'e' imprime acima.
        return f"**Erro na API:** {str(e)}"
   
async def estruturar_plano(texto):
    prompt = f"""
    Você é um Mentor de Impacto Social por IA. Restruture as entradas do usuário em um resumo de plano claro e conciso em markdown. Seja breve!
    **Entrada:**
    Deve conter:
    - Problema
    - Orçamento
    - Tempo
    - Local
    Texto:
    ---------
    {texto}
    ---------
    
    **Saída:** Um plano estruturado em até 100 palavras. Se faltar informação, retorne:
    ---------
    ! Faltam informações: [liste o que falta]
    ---------
    """
    try:
        return await fazer_pergunta(prompt)
    except Exception as e:
        return f"### Resumo do Plano\n**Erro:** {str(e)}"

async def dividir_tarefas(texto):
    prompt = f"""
    Divida o plano em 4–6 passos acionáveis em markdown. Seja breve!
    **Entrada:**
    Deve conter:
    - Problema
    - Orçamento
    - Tempo
    - Local
    Texto:
    ---------
    {texto}
    ---------
    
    **Saída:** Lista de passos em até 100 palavras.
    """
    try:
        return await fazer_pergunta(prompt)
    except Exception as e:
        return f"### Plano de Ação\n**Erro:** {str(e)}"

async def estimar_custos(texto):
    prompt = f"""
    Estime custos para o problema com base no orçamento, em markdown. Seja breve!
    Texto:
    ---------
    {texto}
    ---------
    
    **Saída:** Lista de itens com preços em até 80 palavras.
    """
    try:
        return await fazer_pergunta(prompt)
    except Exception as e:
        return f"### Estimativa de Custos\n**Erro:** {str(e)}"

async def buscar_ongs(texto):
    prompt = f"""
    Sugira 2 ONGs no local para o problema, em markdown. Seja breve!
    Texto:
    ---------
    {texto}
    ---------
    
    **Saída:** Nome, distância, contato e missão de cada ONG, em até 60 palavras.
    """
    try:
        return await fazer_pergunta(prompt)
    except Exception:
        fallback = [
            {"nome": "ONG Genérica 1", "distancia": "Desconhecida", "contato": "contato@ong1.org", "missao": "Apoio geral"},
            {"nome": "ONG Genérica 2", "distancia": "Desconhecida", "contato": "contato@ong2.org", "missao": "Apoio geral"}
        ]
        return "\n".join([
            "### ONGs Sugeridas",
            *[f"- **{ong['nome']}**: {ong['distancia']}, contato: {ong['contato']}, missão: {ong['missao']}" for ong in fallback]
        ])

async def gerar_motivacao(texto):
    prompt = f"""
    Gere uma mensagem motivacional breve sobre o problema no local, em markdown. Máximo 50 palavras.
    Texto:
    ---------
    {texto}
    ---------
    """
    try:
        return await fazer_pergunta(prompt)
    except asyncio.TimeoutError:
        return "**Erro:** Tempo limite excedido"
    except Exception as e:
        return f"### Mensagem Motivacional\nErro: {str(e)}"

class MentorApp(App):
    CSS_PATH = "styles.css"


    def compose(self) -> ComposeResult:
        yield Header()
        with Container(): # Container principal
            with Vertical(): # Container Vertical para empilhar a linha Input/Button e os Statics
                with Horizontal(id="input_row"):
                    yield Input(placeholder="Ex.: Problema: fome, Orçamento: R$100, Tempo: 10h, Local: São Paulo, Progresso: inicial", id="dados_projeto")
                    yield Button("Gerar Plano", id="gerar")
                with Vertical(id="loading_area", classes="-hidden"): # <-- ADICIONADO: Container para loading, invisível por padrão
                     # O widget de status (#status) agora fica DENTRO desta área de loading
                     yield Static("Carregando...", id="status") # <-- MOVIDO: Static#status para dentro de #loading_area
                     yield LoadingIndicator(id="loading_spinner") # <-- ADICIONADO: LoadingIndicator com um ID

                # A área de output principal (será escondida durante loading)
                yield Markdown("", id="output") # <-- Static#output agora vem DEPOIS da área de loading

        yield Footer()


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "gerar":
            gerar_button = self.query_one("#gerar", Button)
            # Obtenha referências para o status (agora dentro da área de loading), output, e a área de loading
            status_widget = self.query_one("#status", Static)
            output_widget = self.query_one("#output", Markdown)
            loading_area = self.query_one("#loading_area", Vertical) # <-- ADICIONADO

            gerar_button.disabled = True # Desabilita o botão

            # --- Lógica para esconder output e mostrar área de loading ---
            output_widget.add_class("-hidden") # <-- ADICIONADO: Esconde o output
            loading_area.remove_class("-hidden") # <-- ADICIONADO: Mostra a área de loading

            status_widget.update("Iniciando...") # Atualiza o status (agora visível na área de loading)
            output_widget.update("") # Limpa o output antigo

            # Cria a tarefa assíncrona, passando o botão
            asyncio.create_task(self.gerar_resposta(gerar_button))

    async def gerar_resposta(self, gerar_button: Button):
        text = self.query_one("#dados_projeto", Input).value
        status_widget = self.query_one("#status", Static) # <-- Referência ao status (dentro de #loading_area)
        output_widget = self.query_one("#output", Markdown)
        loading_area = self.query_one("#loading_area", Vertical) # <-- ADICIONADO: Referência à área de loading

        try:

            status_widget.update("Gerando plano")
            plano = await estruturar_plano(text) # Confirme se client/model_name são globais ou passados
            await asyncio.sleep(0.1)

            # Progresso: Dividir tarefas
            status_widget.update("Dividindo tarefas")
            tarefas = await dividir_tarefas(plano) # Confirme se client/model_name são globais ou passados
            await asyncio.sleep(0.1)

            # Progresso: Estimar custos
            status_widget.update("Gerando orçamento")
            custos = await estimar_custos(plano) # Confirme se client/model_name são globais ou passados
            await asyncio.sleep(0.1)

            # Progresso: Buscar ONGs
            status_widget.update("Buscando ONGs")
            ongs = await buscar_ongs(text) # Confirme se client/model_name são globais ou passados
            await asyncio.sleep(0.1)

            # Progresso: Gerar motivação
            status_widget.update("Criando mensagem motivacional")
            motivacao = await gerar_motivacao(text) # Confirme se client/model_name são globais ou passados
            status_widget.update("Pronto para exibir") # Status atualizado antes de juntar
            await asyncio.sleep(0.1) # Pequeno delay antes de juntar/exibir

            # Finalizado
            output = "\n\n".join([plano, tarefas, custos, ongs, motivacao])
            status_widget.update("Juntando resultados")

            # --- Bloco TRY/EXCEPT existente para isolar erro de exibição ---
            try:
                 output_widget.update(output)
                 status_widget.update("Concluído!")
            except Exception as e:
                 status_widget.update("Erro ao exibir!")
                 print(f"ERRO ao atualizar o widget de saída: {e}")
                 traceback.print_exc()
                 output_widget.update(f"Ocorreu um erro interno ao exibir o resultado:\n{e}\nVerifique a saída do terminal para detalhes.")

        except Exception as e:
            # Este bloco captura erros que acontecem DURANTE as chamadas da API
            status_widget.update("Erro Crítico!")
            output_widget.update(f"Ocorreu um erro crítico durante a geração: {e}\nVerifique o terminal para detalhes.")
            print(f"Erro Crítico na geração: {e}")
            traceback.print_exc()

        finally:
            loading_area.add_class("-hidden") # <-- ADICIONADO: Esconde a área de loading
            output_widget.remove_class("-hidden") # <-- ADICIONADO: Mostra o output principal

            gerar_button.disabled = False # Reativa o botão
            status_widget.update("Pronto??") # Opcional: Reseta o texto de status no Static#status
if __name__ == "__main__":
    MentorApp().run()
