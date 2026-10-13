# 🔔 Alerta de Vagas Júnior/Estágio em Dev

Script Python que busca vagas de **desenvolvedor júnior e estágio** em sites de emprego e envia um e-mail automático com as novidades — sem reenviar o que você já viu.

Roda automaticamente toda semana via **GitHub Actions**, sem precisar deixar o PC ligado.

---

## O que o projeto faz

1. **Busca** vagas no BNE e no Vagas.com
2. **Filtra** por nível (júnior/estágio), área (dev/programação) e região
3. **Lembra** quais vagas já foram enviadas (não repete)
4. **Envia um e-mail** com apenas as vagas novas
5. **Salva o histórico** automaticamente no repositório

---

## Filtros aplicados

| Critério | Valores aceitos |
|---|---|
| **Nível** | Júnior, Jr, Estágio, Estagiário, Trainee, Aprendiz |
| **Área** | Desenvolvedor, Programador, Dev, Software, TI, Web, Mobile, Dados... |
| **Regiões** | Novo Hamburgo, Parobé, Taquara, Igrejinha, São Leopoldo, Sapucaia do Sul, Esteio, Canoas, Porto Alegre |
| **Modalidade** | Remoto, Híbrido e Presencial (nas regiões acima) |

> Vagas sem localização definida são aceitas por padrão (benefício da dúvida).

---

## Estrutura do projeto

```
alerta-vagas/
├── main.py            # Orquestra tudo — ponto de entrada
├── buscar.py          # Baixa e extrai vagas do BNE e Vagas.com
├── filtrar.py         # Filtra por nível, área, região e modalidade
├── memoria.py         # Lê e grava o histórico de vagas já enviadas
├── email_alerta.py    # Monta e envia o e-mail (texto + HTML)
├── vistas.json        # Histórico de links já enviados
├── requirements.txt   # Dependências: requests, beautifulsoup4
└── .github/
    └── workflows/
        └── vagas.yml  # Agendamento automático (GitHub Actions)
```

---

## Como rodar localmente

```bash
pip install -r requirements.txt

# Windows (PowerShell)
$env:GMAIL_USER = "seuemail@gmail.com"
$env:GMAIL_APP_PASSWORD = "sua-senha-de-app"

python main.py
```

---

## Como automatizar no GitHub

1. Suba o projeto no GitHub
2. Vá em **Settings → Secrets and variables → Actions**
3. Crie dois secrets:

| Nome | Valor |
|---|---|
| `GMAIL_USER` | seu e-mail Gmail |
| `GMAIL_APP_PASSWORD` | senha de app gerada em [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) |

4. Vá em **Actions → Buscar vagas → Run workflow** para testar

O script roda automaticamente toda **segunda-feira às 8h (horário de Brasília)**.

---

## Dependências

- [`requests`](https://requests.readthedocs.io) — faz o download das páginas
- [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — extrai as vagas do HTML
- `smtplib` e `email` — enviam o e-mail (já vêm com o Python)
- `sqlite3` / `json` — guardam o histórico (já vêm com o Python)