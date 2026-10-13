"""
filtrar.py — mantém só as vagas de nível júnior ou estágio na área de dev,
nas regiões aceitas e nas modalidades desejadas.

Critério:
  - Título tem palavra de NÍVEL (júnior, estágio...) E palavra de ÁREA (dev...)
  - Campo "local" está em uma das REGIÕES aceitas OU é remoto/híbrido
  - Se o campo local não tiver informação suficiente, a vaga é aceita
    (benefício da dúvida — melhor ver uma vaga a mais do que perder uma boa)
"""

import unicodedata


# ── Nível de entrada ────────────────────────────────────────────────────────
PALAVRAS_NIVEL = [
    "junior", "jr",
    "estagio", "estagiario", "estagiaria",
    "trainee", "aprendiz",
]

# ── Área de tecnologia ───────────────────────────────────────────────────────
PALAVRAS_AREA = [
    "desenvolvedor", "desenvolvedora", "desenvolvimento",
    "programador", "programadora", "programacao",
    "dev", "software", "sistemas",
    "ti", "tecnologia", "informatica",
    "backend", "back-end",
    "frontend", "front-end",
    "fullstack", "full stack", "full-stack",
    "web", "mobile",
    "dados", "data",
    "python", "java", "javascript", "react", "node",
]

# ── Regiões aceitas ──────────────────────────────────────────────────────────
# Palavras que devem aparecer no campo "local" para a vaga ser aceita.
REGIOES_ACEITAS = [
    "novo hamburgo",
    "parobé", "parobe",
    "sao leopoldo", "são leopoldo",
    "sapucaia do sul", "sapucaia",
    "esteio",
    "canoas",
    "porto alegre",
    # Estado genérico — aceita quando só diz RS sem especificar cidade
    ", rs",
    "rio grande do sul",
]

# ── Modalidades aceitas ──────────────────────────────────────────────────────
# Vagas com essas palavras no campo "local" são aceitas independente da cidade.
MODALIDADES_ACEITAS = [
    "remoto", "remote",
    "hibrido", "híbrido", "hybrid",
    "home office", "homeoffice",
]


# ── Utilitários ─────────────────────────────────────────────────────────────

def _normalizar(texto: str) -> str:
    """Converte para minúsculas e remove acentos para facilitar a comparação."""
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


def _contem_alguma(texto_norm: str, palavras: list[str]) -> bool:
    """Retorna True se o texto normalizado contiver ao menos uma das palavras."""
    return any(palavra in texto_norm for palavra in palavras)


def _local_aceito(local: str) -> bool:
    """
    Retorna True se o campo 'local' da vaga for aceito.

    Aceita se:
      - For remoto, híbrido ou home office  (modalidade)
      - Estiver em uma das regiões aceitas  (localização)
      - Campo local estiver vazio ou vago   (benefício da dúvida)
    """
    local_norm = _normalizar(local)

    # Campo vazio ou genérico → aceita (não sabemos onde é)
    if not local_norm or local_norm in ("nao informado", "a definir", "-"):
        return True

    # Modalidade remota/híbrida → aceita independente da cidade
    if _contem_alguma(local_norm, [_normalizar(m) for m in MODALIDADES_ACEITAS]):
        return True

    # Região aceita
    if _contem_alguma(local_norm, [_normalizar(r) for r in REGIOES_ACEITAS]):
        return True

    return False


# ── Filtro principal ─────────────────────────────────────────────────────────

def filtrar(vagas: list[dict]) -> list[dict]:
    """
    Filtra as vagas por nível de entrada, área de dev, região e modalidade.

    Parâmetros
    ----------
    vagas : list[dict]
        Lista de dicionários com as chaves titulo, empresa, local, link, fonte.

    Retorno
    -------
    list[dict]
        Subconjunto das vagas que passaram em todos os critérios.
    """
    selecionadas = []
    for vaga in vagas:
        titulo_norm = _normalizar(vaga.get("titulo", ""))

        eh_nivel_entrada = _contem_alguma(titulo_norm, PALAVRAS_NIVEL)
        eh_area_dev      = _contem_alguma(titulo_norm, PALAVRAS_AREA)
        local_ok         = _local_aceito(vaga.get("local", ""))

        if eh_nivel_entrada and eh_area_dev and local_ok:
            selecionadas.append(vaga)

    print(f"[filtrar] {len(selecionadas)} vagas após o filtro (de {len(vagas)} encontradas).")
    return selecionadas
