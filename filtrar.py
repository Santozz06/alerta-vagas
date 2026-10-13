"""
filtrar.py — mantém só as vagas de nível júnior ou estágio na área de dev.

Critério: o título precisa ter pelo menos UMA palavra de nível E pelo menos
UMA palavra de área. Maiúsculas e acentos são ignorados.
"""

import unicodedata


# Palavras que indicam nível de entrada
PALAVRAS_NIVEL = [
    "junior",
    "júnior",
    "jr",
    "estagio",
    "estágio",
    "estagiario",
    "estagiário",
    "trainee",
    "aprendiz",
]

# Palavras que indicam área de tecnologia / desenvolvimento
PALAVRAS_AREA = [
    "desenvolvedor",
    "desenvolvimento",
    "programador",
    "programacao",
    "programação",
    "dev",
    "software",
    "sistemas",
    "ti ",
    "tecnologia",
    "backend",
    "front",
    "fullstack",
    "full stack",
    "web",
    "mobile",
    "dados",
    "data",
    "python",
    "java",
    "javascript",
    "react",
    "node",
]


def _normalizar(texto: str) -> str:
    """
    Converte para minúsculas e remove acentos, facilitando a comparação.

    Exemplo: 'Estágio' → 'estagio'
    """
    texto = texto.lower()
    # Decompõe caracteres acentuados e remove os diacríticos
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


def _contem_alguma(texto_norm: str, palavras: list[str]) -> bool:
    """Retorna True se o texto normalizado contiver ao menos uma das palavras."""
    return any(palavra in texto_norm for palavra in palavras)


def filtrar(vagas: list[dict]) -> list[dict]:
    """
    Recebe a lista completa de vagas e devolve só as de júnior/estágio em dev.

    Parâmetros
    ----------
    vagas : list[dict]
        Lista de dicionários com pelo menos a chave 'titulo'.

    Retorno
    -------
    list[dict]
        Subconjunto das vagas que passaram no filtro.
    """
    selecionadas = []
    for vaga in vagas:
        titulo_norm = _normalizar(vaga.get("titulo", ""))
        eh_nivel_entrada = _contem_alguma(titulo_norm, PALAVRAS_NIVEL)
        eh_area_dev = _contem_alguma(titulo_norm, PALAVRAS_AREA)

        if eh_nivel_entrada and eh_area_dev:
            selecionadas.append(vaga)

    print(f"[filtrar] {len(selecionadas)} vagas após o filtro (de {len(vagas)} encontradas).")
    return selecionadas
