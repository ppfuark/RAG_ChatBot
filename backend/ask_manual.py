import asyncio
import httpx
from rich import print  # Para melhor formatação (instale com: pip install rich)

# Configurações
API_URL = "http://localhost:8000/api/query"
TIMEOUT = 100.0  # segundos

# Lista de perguntas
PERGUNTAS = [
    "Quais são as regras de vestimenta obrigatórias para os aprendizes?",
    "Como deve ser feito o descarte de lixo segundo o manual?",
    "O que é o 5S e quando ele deve ser realizado na ETS?",
]

async def enviar_pergunta(client: httpx.AsyncClient, pergunta: str):
    try:
        resposta = await client.post(
            API_URL,
            json={"question": pergunta},
            timeout=TIMEOUT
        )
        resposta.raise_for_status()
        dados = resposta.json()
        
        return {
            "sucesso": True,
            "pergunta": pergunta,
            "resposta": dados.get("answer", "Resposta não encontrada"),
            "fontes": dados.get("sources", [])
        }
    except Exception as erro:
        return {
            "sucesso": False,
            "pergunta": pergunta,
            "erro": str(erro),
            "status_code": getattr(erro.response, "status_code", None) if isinstance(erro, httpx.HTTPStatusError) else None
        }

async def main():
    print(f"[bold]Iniciando teste com {len(PERGUNTAS)} perguntas...[/bold]")
    
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resultados = await asyncio.gather(*[enviar_pergunta(client, p) for p in PERGUNTAS])
        
        sucessos = sum(1 for r in resultados if r["sucesso"])
        falhas = len(PERGUNTAS) - sucessos
        
        print(f"\n[bold]Resumo:[/bold]")
        print(f"✅ [green]Sucessos: {sucessos}[/green]")
        print(f"❌ [red]Falhas: {falhas}[/red]")
        
        print("\n[bold]Detalhes:[/bold]")
        for resultado in resultados:
            if resultado["sucesso"]:
                print(f"\n[bold cyan]Pergunta:[/bold cyan] {resultado['pergunta']}")
                print(f"[green]Resposta:[/green] {resultado['resposta']}")
                if resultado["fontes"]:
                    print(f"[dim]Fontes: {', '.join(resultado['fontes'])}[/dim]")
            else:
                print(f"\n[bold red]Falha:[/bold red] {resultado['pergunta']}")
                if resultado.get("status_code"):
                    print(f"[red]HTTP {resultado['status_code']}: {resultado['erro']}[/red]")
                else:
                    print(f"[red]Erro: {resultado['erro']}[/red]")

if __name__ == "__main__":
    asyncio.run(main())