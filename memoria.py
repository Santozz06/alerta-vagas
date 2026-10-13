"""
memoria.py — lê e grava o arquivo vistas.json com os links já enviados.

O arquivo guarda uma lista de strings (URLs). A cada execução:
  1. Carregamos os links já conhecidos.
  2. Separamos as vagas novas das já vistas.
  3. Após o envio, adicionamos os links novos ao arquivo.
"""

import json
from pathlib import Path

# Caminho do arquivo relativo a este script
ARQUIVO_VISTAS = Path(__file__).parent / "vistas.json"


def carregar_vistas() -> set[str]:
    """
    Lê o arquivo vistas.json e retorna um conjunto de links já enviados.

    Retorna um conjunto vazio se o arquivo não existir ou estiver vazio.
    """
    if not ARQUIVO_VISTAS.exists():
        return set()

    try:
        conteudo = ARQUIVO_VISTAS.read_text(encoding="utf-8").strip()
        if not conteudo:
            return set()
        return set(json.loads(conteudo))
    except (json.JSONDecodeError, OSError) as erro:
        print(f"[memoria] Aviso: não foi possível ler {ARQUIVO_VISTAS}: {erro}")
        return set()


def salvar_vistas(links: set[str]) -> None:
    """
    Sobrescreve o arquivo vistas.json com o conjunto de links recebido.

    Parâmetros
    ----------
    links : set[str]
        Conjunto completo de links já enviados (incluindo os novos).
    """
    try:
        ARQUIVO_VISTAS.write_text(
            json.dumps(sorted(links), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError as erro:
        print(f"[memoria] Erro ao salvar {ARQUIVO_VISTAS}: {erro}")


def separar_novas(vagas: list[dict], vistas: set[str]) -> list[dict]:
    """
    Retorna somente as vagas cujo link ainda não está em `vistas`.

    Parâmetros
    ----------
    vagas  : lista completa de vagas filtradas
    vistas : conjunto de links já enviados

    Retorno
    -------
    list[dict] com as vagas inéditas
    """
    novas = [v for v in vagas if v["link"] not in vistas]
    print(f"[memoria] {len(novas)} vagas novas (de {len(vagas)} filtradas).")
    return novas


def marcar_como_vistas(vagas: list[dict], vistas: set[str]) -> set[str]:
    """
    Adiciona os links das vagas ao conjunto `vistas` e salva no disco.

    Parâmetros
    ----------
    vagas  : vagas que acabaram de ser enviadas
    vistas : conjunto atual de links vistos

    Retorno
    -------
    set[str] atualizado
    """
    novos_links = {v["link"] for v in vagas}
    vistas_atualizadas = vistas | novos_links
    salvar_vistas(vistas_atualizadas)
    print(f"[memoria] {len(novos_links)} links adicionados ao histórico.")
    return vistas_atualizadas
