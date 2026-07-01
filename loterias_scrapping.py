"""
WEB SCRAPPING USANDO API REST
"""

import requests
from openpyxl import Workbook
from datetime import datetime

# A Caixa expõe os resultados das loterias através dessa API pública (a mesma
# que o site https://loterias.caixa.gov.br usa por baixo dos panos), então não
# precisamos de Selenium/HTML scraping aqui: uma chamada HTTP simples por jogo
# já retorna os dados estruturados em JSON, muito mais rápido e estável do que
# raspar a página Angular do site.
API_BASE = "https://servicebus2.caixa.gov.br/portaldeloterias/api"

MODALIDADES = {
    "megasena": "Mega-Sena",
    "lotofacil": "Lotofácil",
    "quina": "Quina",
    "lotomania": "Lotomania",
    "timemania": "Timemania",
    "duplasena": "Dupla Sena",
    "diadesorte": "Dia de Sorte",
    "supersete": "Super Sete",
    "maismilionaria": "+Milionária",
    "federal": "Loteria Federal",
}

COLUNAS = [
    "Nome do Jogo",
    "Valor do Prêmio",
    "Resultado",
    "Acumulou",
    "Data do Concurso",
    "Código do Concurso",
    "Próximo Sorteio",
]

def buscar_resultado(slug):
    resposta = requests.get(f"{API_BASE}/{slug}", timeout=15)
    resposta.raise_for_status()
    return resposta.json()

def extrair_dados(nome_jogo, resultado):
    # Valor do prêmio = valor pago para quem acertou a faixa máxima (todos os
    # números) nesse concurso. Quando o concurso acumula, esse valor fica 0 e
    # o prêmio real passa para "Próximo Sorteio".
    premiacoes = resultado.get("listaRateioPremio") or []
    valor_premio = premiacoes[0]["valorPremio"] if premiacoes else 0.0

    dezenas = resultado.get("listaDezenas") or []

    return {
        "Nome do Jogo": nome_jogo,
        "Valor do Prêmio": valor_premio,
        "Resultado": ", ".join(dezenas),
        "Acumulou": "Sim" if resultado.get("acumulado") else "Não",
        "Data do Concurso": resultado.get("dataApuracao"),
        "Código do Concurso": resultado.get("numero"),
        "Próximo Sorteio": resultado.get("dataProximoConcurso"),
    }

def coletar_todos_os_jogos():
    dados = []
    for slug, nome_jogo in MODALIDADES.items():
        print(f"Buscando resultado de {nome_jogo}...")
        try:
            resultado = buscar_resultado(slug)
            dados.append(extrair_dados(nome_jogo, resultado))
        except Exception as e:
            print(f"Falha ao buscar {nome_jogo}: {e}")
    return dados

def salvar_excel(dados):
    workbook = Workbook()
    planilha = workbook.active
    planilha.title = "Resultados"
    planilha.append(COLUNAS)

    for linha in dados:
        planilha.append([linha[coluna] for coluna in COLUNAS])

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"resultados_loterias_{timestamp}.xlsx"
    workbook.save(nome_arquivo)
    print(f"Arquivo salvo: {nome_arquivo}")

def main():
    dados = coletar_todos_os_jogos()
    if not dados:
        print("Nenhum resultado coletado.")
        return
    salvar_excel(dados)

if __name__ == "__main__":
    main()
