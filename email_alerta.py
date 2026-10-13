"""
email_alerta.py — monta e envia o e-mail com as vagas novas.

Credenciais são lidas via variáveis de ambiente:
  GMAIL_USER         → seu endereço Gmail (ex.: seunome@gmail.com)
  GMAIL_APP_PASSWORD → senha de app gerada em myaccount.google.com/apppasswords

No Google Colab, use:
  from google.colab import userdata
  os.environ["GMAIL_USER"] = userdata.get("GMAIL_USER")
  os.environ["GMAIL_APP_PASSWORD"] = userdata.get("GMAIL_APP_PASSWORD")

No GitHub Actions, defina os Secrets no repositório e passe via env: no workflow.
"""

import os
import smtplib
from email.message import EmailMessage


def _montar_texto(vagas: list[dict]) -> str:
    """Formata a lista de vagas como texto simples para o corpo do e-mail."""
    linhas = ["Olá! Aqui estão as novas vagas júnior/estágio em dev encontradas hoje:\n"]
    for i, vaga in enumerate(vagas, start=1):
        linhas.append(
            f"{i}. {vaga['titulo']}\n"
            f"   Empresa : {vaga['empresa']}\n"
            f"   Local   : {vaga['local']}\n"
            f"   Fonte   : {vaga['fonte']}\n"
            f"   Link    : {vaga['link']}\n"
        )
    linhas.append("\nBoa sorte nas candidaturas!")
    return "\n".join(linhas)


def _montar_html(vagas: list[dict]) -> str:
    """Formata a lista de vagas como HTML para uma versão mais bonita do e-mail."""
    itens = ""
    for vaga in vagas:
        itens += (
            f"<li style='margin-bottom:16px;'>"
            f"<strong><a href='{vaga['link']}' style='color:#2563eb;'>{vaga['titulo']}</a></strong><br>"
            f"🏢 {vaga['empresa']} &nbsp;|&nbsp; 📍 {vaga['local']} &nbsp;|&nbsp; 🔗 {vaga['fonte']}"
            f"</li>"
        )

    return f"""
    <html>
    <body style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1e293b;">
      <h2 style="color:#2563eb;">🔔 Novas vagas júnior/estágio em dev</h2>
      <p>Olá! Encontrei <strong>{len(vagas)}</strong> vaga(s) nova(s) para você:</p>
      <ul style="padding-left:20px;">
        {itens}
      </ul>
      <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0;">
      <p style="font-size:12px;color:#64748b;">
        Gerado automaticamente pelo alerta-vagas 🤖
      </p>
    </body>
    </html>
    """


def enviar_email(vagas: list[dict]) -> bool:
    """
    Envia o e-mail de alerta com as vagas novas.

    Parâmetros
    ----------
    vagas : lista de dicionários de vagas novas

    Retorno
    -------
    True se o envio foi bem-sucedido, False caso contrário.
    """
    remetente = os.environ.get("GMAIL_USER", "").strip()
    senha_app = os.environ.get("GMAIL_APP_PASSWORD", "").strip()

    if not remetente or not senha_app:
        print(
            "[email] ERRO: variáveis GMAIL_USER e/ou GMAIL_APP_PASSWORD não definidas.\n"
            "  → No terminal local: set GMAIL_USER=seuemail@gmail.com\n"
            "  → No GitHub Actions: defina os Secrets no repositório."
        )
        return False

    assunto = f"🔔 {len(vagas)} nova(s) vaga(s) júnior/estágio em dev"

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = remetente  # Envia para você mesmo; mude se precisar
    msg.set_content(_montar_texto(vagas))          # versão texto simples
    msg.add_alternative(_montar_html(vagas), subtype="html")  # versão HTML

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remetente, senha_app)
            servidor.send_message(msg)
        print(f"[email] E-mail enviado para {remetente} com {len(vagas)} vaga(s).")
        return True
    except smtplib.SMTPAuthenticationError:
        print(
            "[email] ERRO de autenticação. Verifique se:\n"
            "  1. A verificação em duas etapas está ativada na conta Google.\n"
            "  2. Você está usando uma senha de APP (não a senha normal da conta).\n"
            "  3. Gere a senha em: https://myaccount.google.com/apppasswords"
        )
        return False
    except smtplib.SMTPException as erro:
        print(f"[email] Erro ao enviar e-mail: {erro}")
        return False
