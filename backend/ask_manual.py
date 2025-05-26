import asyncio
import httpx
from rich import print  # Formatação bonita no terminal

# Configurações
API_URL = "http://127.0.0.1:8000/rag/ask"
TIMEOUT = 30.0  # segundos

# Perguntas a serem feitas
PERGUNTAS = [
    "Quando o homem foi a lua?"
]

async def enviar_pergunta(pergunta: str):
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            resposta = await client.post(API_URL, json={"question": pergunta})
            resposta.raise_for_status()
            dados = resposta.json()

            return {
                "sucesso": True,
                "pergunta": pergunta,
                "resposta": dados.get("answer", "Sem resposta")
            }
        except httpx.HTTPStatusError as e:
            return {
                "sucesso": False,
                "pergunta": pergunta,
                "erro": f"HTTP {e.response.status_code}: {e.response.text}"
            }
        except Exception as e:
            return {
                "sucesso": False,
                "pergunta": pergunta,
                "erro": str(e)
            }

async def main():
    print(f"[bold]Consultando API com {len(PERGUNTAS)} perguntas...[/bold]")

    resultados = await asyncio.gather(*[enviar_pergunta(p) for p in PERGUNTAS])

    print("\n[bold]Resumo:[/bold]")
    for r in resultados:
        if r["sucesso"]:
            print(f"\n[cyan]Pergunta:[/cyan] {r['pergunta']}")
            print(f"[green]Resposta:[/green] {r['resposta']}")
        else:
            print(f"\n[red]Erro na pergunta:[/red] {r['pergunta']}")
            print(f"[red]Detalhes:[/red] {r['erro']}")

if __name__ == "__main__":
    asyncio.run(main())
