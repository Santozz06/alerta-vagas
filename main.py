"""
main.py — ponto de entrada do alerta de vagas.

Execução:
  python main.py

Fluxo:
  1. Busca vagas no BNE e no Vagas.com.
  2. Filtra pelas palavras de nível e área.
  3. Separa as vagas novas das que já foram enviadas.
  4. Envia o e-mail (se houver vagas novas).
  5. Salva os links enviados no histórico.
"""

import sys

from buscar import buscar_todas
from filtrar import filtrar
from memoria import carregar_vistas, separar_novas, marcar_como_vistas
from email_alerta import enviar_email


def main() -> None:
    print("=" * 50)
    print("  Alerta de Vagas Júnior/Estágio em Dev")
    print("=" * 50)

    # 1. Buscar
    todas_as_vagas = buscar_todas()

    if not todas_as_vagas:
        print("\n[main] Nenhuma vaga encontrada. Encerrando.")
        sys.exit(0)

    # 2. Filtrar
    vagas_filtradas = filtrar(todas_as_vagas)

    if not vagas_filtradas:
        print("\n[main] Nenhuma vaga passou no filtro. Encerrando.")
        sys.exit(0)

    # 3. Separar novas
    vistas = carregar_vistas()
    vagas_novas = separar_novas(vagas_filtradas, vistas)

    if not vagas_novas:
        print("\n[main] Sem vagas novas desta vez. Até a próxima!")
        sys.exit(0)

    # 4. Enviar e-mail
    enviado = enviar_email(vagas_novas)

    # 5. Salvar histórico (só se o envio foi bem-sucedido)
    if enviado:
        marcar_como_vistas(vagas_novas, vistas)
    else:
        print("\n[main] E-mail não enviado. Histórico não foi atualizado.")
        sys.exit(1)

    print("\n[main] Concluído com sucesso! ✅")


if __name__ == "__main__":
    main()
