"""
buscar.py — baixa páginas de vagas e extrai título, empresa, local e link.

Fontes suportadas:
  - BNE (bne.com.br)
  - Vagas.com (vagas.com)

Se o site mudar o layout, volte aqui, inspecione o HTML com o navegador
e atualize os seletores nas funções buscar_bne() e buscar_vagas_com().
"""

import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# Pausa entre requisições para não sobrecarregar os sites
PAUSA_SEGUNDOS = 2


def _get(url: str) -> BeautifulSoup | None:
    """Faz o GET e retorna um BeautifulSoup, ou None em caso de erro."""
    try:
        resposta = requests.get(url, headers=HEADERS, timeout=30)
        resposta.raise_for_status()
        return BeautifulSoup(resposta.text, "html.parser")
    except requests.RequestException as erro:
        print(f"  [AVISO] Erro ao acessar {url}: {erro}")
        return None


# ---------------------------------------------------------------------------
# BNE
# ---------------------------------------------------------------------------

# URLs do BNE a serem raspadadas.
# Adicione mais cidades ou termos de busca conforme precisar.
URLS_BNE = [
    # Novo Hamburgo
    "https://www.bne.com.br/vagas-de-emprego-para-desenvolvedor-em-novo-hamburgo-rs",
    "https://www.bne.com.br/vagas-de-emprego-para-programador-em-novo-hamburgo-rs",
    # Parobé
    "https://www.bne.com.br/vagas-de-emprego-para-desenvolvedor-em-parobe-rs",
    # Taquara
    "https://www.bne.com.br/vagas-de-emprego-para-desenvolvedor-em-taquara-rs",
    # Igrejinha
    "https://www.bne.com.br/vagas-de-emprego-para-desenvolvedor-em-igrejinha-rs",
    # São Leopoldo
    "https://www.bne.com.br/vagas-de-emprego-para-desenvolvedor-em-sao-leopoldo-rs",
    # Sapucaia do Sul
    "https://www.bne.com.br/vagas-de-emprego-para-desenvolvedor-em-sapucaia-do-sul-rs",
    # Esteio
    "https://www.bne.com.br/vagas-de-emprego-para-desenvolvedor-em-esteio-rs",
    # Canoas
    "https://www.bne.com.br/vagas-de-emprego-para-desenvolvedor-em-canoas-rs",
    # Porto Alegre
    "https://www.bne.com.br/vagas-de-emprego-para-desenvolvedor-em-porto-alegre-rs",
    # Remoto (RS)
    "https://www.bne.com.br/vagas-de-emprego-para-desenvolvedor-home-office",
]


def buscar_bne() -> list[dict]:
    """
    Raspa as URLs do BNE e retorna uma lista de vagas.

    Cada vaga é um dicionário com as chaves:
      titulo, empresa, local, link, fonte
    """
    vagas = []
    for url in URLS_BNE:
        print(f"  Buscando BNE: {url}")
        soup = _get(url)
        if soup is None:
            continue

        # -------------------------------------------------------------------
        # SELETORES DO BNE — ajuste aqui se o site mudar o layout.
        #
        # Para encontrar os seletores certos:
        #   1. Abra a URL no navegador.
        #   2. Clique com botão direito em uma vaga → "Inspecionar".
        #   3. Identifique a tag e a classe que envolve cada vaga.
        # -------------------------------------------------------------------
        cartoes = soup.select("article.vaga, div.vaga-item, li.job-item")

        if not cartoes:
            # Tentativa genérica: procura links que contenham "/vaga/" na URL
            cartoes = [
                a.parent
                for a in soup.find_all("a", href=True)
                if "/vaga/" in a["href"]
            ]

        for cartao in cartoes:
            link_tag = cartao.find("a", href=True)
            if link_tag is None:
                continue

            link = link_tag["href"]
            if not link.startswith("http"):
                link = "https://www.bne.com.br" + link

            titulo = (
                cartao.find(class_=lambda c: c and "titulo" in c.lower())
                or cartao.find("h2")
                or cartao.find("h3")
                or link_tag
            )
            titulo = titulo.get_text(strip=True) if titulo else "Sem título"

            empresa = cartao.find(class_=lambda c: c and "empresa" in c.lower())
            empresa = empresa.get_text(strip=True) if empresa else "Não informada"

            local = cartao.find(class_=lambda c: c and ("local" in c.lower() or "cidade" in c.lower()))
            local = local.get_text(strip=True) if local else "Não informado"

            vagas.append({
                "titulo": titulo,
                "empresa": empresa,
                "local": local,
                "link": link,
                "fonte": "BNE",
            })

        time.sleep(PAUSA_SEGUNDOS)

    return vagas


# ---------------------------------------------------------------------------
# Vagas.com
# ---------------------------------------------------------------------------

# Termos de busca no Vagas.com. Adicione ou remova conforme precisar.
BUSCAS_VAGAS_COM = [
    "https://www.vagas.com.br/vagas-de-desenvolvedor-junior",
    "https://www.vagas.com.br/vagas-de-estagio-em-desenvolvimento",
]


def buscar_vagas_com() -> list[dict]:
    """
    Raspa o Vagas.com e retorna uma lista de vagas.

    Cada vaga é um dicionário com as chaves:
      titulo, empresa, local, link, fonte
    """
    vagas = []
    for url in BUSCAS_VAGAS_COM:
        print(f"  Buscando Vagas.com: {url}")
        soup = _get(url)
        if soup is None:
            continue

        # -------------------------------------------------------------------
        # SELETORES DO VAGAS.COM — ajuste aqui se o site mudar o layout.
        # -------------------------------------------------------------------
        cartoes = soup.select("li.vaga, article.vaga, div.job-item")

        for cartao in cartoes:
            link_tag = cartao.find("a", href=True)
            if link_tag is None:
                continue

            link = link_tag["href"]
            if not link.startswith("http"):
                link = "https://www.vagas.com.br" + link

            titulo = (
                cartao.find("h2")
                or cartao.find("h3")
                or cartao.find(class_=lambda c: c and "cargo" in c.lower())
                or link_tag
            )
            titulo = titulo.get_text(strip=True) if titulo else "Sem título"

            empresa = cartao.find(class_=lambda c: c and "empresa" in c.lower())
            empresa = empresa.get_text(strip=True) if empresa else "Não informada"

            local = cartao.find(class_=lambda c: c and ("local" in c.lower() or "cidade" in c.lower()))
            local = local.get_text(strip=True) if local else "Não informado"

            vagas.append({
                "titulo": titulo,
                "empresa": empresa,
                "local": local,
                "link": link,
                "fonte": "Vagas.com",
            })

        time.sleep(PAUSA_SEGUNDOS)

    return vagas


# ---------------------------------------------------------------------------
# Ponto de entrada principal
# ---------------------------------------------------------------------------

def buscar_todas() -> list[dict]:
    """Busca vagas em todas as fontes e retorna a lista completa."""
    print("[buscar] Iniciando busca de vagas...")
    vagas = []
    vagas.extend(buscar_bne())
    vagas.extend(buscar_vagas_com())
    print(f"[buscar] {len(vagas)} vagas encontradas no total.")
    return vagas
