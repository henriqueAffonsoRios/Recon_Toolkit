# 🔍 Recon Toolkit

Ferramenta educacional de reconhecimento para a fase inicial de testes de penetração (pentest).

> ⚠️ **Aviso legal:** Esta ferramenta foi desenvolvida exclusivamente para fins educacionais.
> Utilize apenas em sistemas próprios ou com autorização explícita do proprietário.
> O uso não autorizado pode constituir crime conforme a Lei nº 12.737/2012 (Lei Carolina Dieckmann).

---

## 📌 O que é

O Recon Toolkit automatiza a fase de reconhecimento de um pentest, coletando informações
sobre um alvo a partir de fontes públicas e técnicas passivas/ativas controladas.

Essa é a **primeira etapa da metodologia de pentest** — antes de qualquer exploração,
um profissional precisa mapear a superfície de ataque do alvo.

---

## ⚙️ Módulos

| Módulo | Descrição |
|---|---|
| **Port Scanner** | Identifica portas TCP abertas via conexão paralela |
| **Banner Grabbing** | Extrai versão dos serviços nas portas abertas |
| **DNS Enumeration** | Consulta registros A, MX, NS, TXT e CNAME |
| **Subdomain Enumeration** | Descobre subdomínios via wordlist com detecção de wildcard DNS |
| **HTTP Security Headers** | Analisa presença de headers de segurança (OWASP) |
| **WHOIS Lookup** | Coleta dados públicos de registro do domínio |
| **Report Generator** | Gera relatório estruturado em JSON e TXT |

---

## 🚀 Como usar

**Instalação:**
```bash
git clone https://github.com/henriqueAffonsoRios/recon-toolkit
cd recon-toolkit
pip install -r requirements.txt
```

**Uso básico:**
```bash
python main.py --target exemplo.com
```

**Com range de portas customizado:**
```bash
python main.py --target exemplo.com --ports 1-1024
```

**Com wordlist customizada:**
```bash
python main.py --target exemplo.com --wordlist wordlist/subdomains.txt
```

---

## 📄 Relatório gerado

Ao finalizar, a ferramenta salva automaticamente dois arquivos na pasta `reports/`:

- `report_<alvo>_<timestamp>.json` — dados estruturados para integração com outras ferramentas
- `report_<alvo>_<timestamp>.txt` — resumo legível para documentação

---

## 🛠️ Tecnologias

- Python 3.14+
- `socket` — port scanning e banner grabbing
- `dnspython` — enumeração de DNS
- `requests` — análise de headers HTTP
- `python-whois` — consulta WHOIS
- `concurrent.futures` — paralelismo no port scanner e subdomain enum
- `colorama` — output colorido no terminal

---

## 📁 Estrutura do projeto

```
recon_toolkit/
├── modules/
│   ├── port_scanner.py
│   ├── banner_grabber.py
│   ├── dns_enum.py
│   ├── subdomain_enum.py
│   ├── http_headers.py
│   └── whois_lookup.py
├── utils/
│   └── reporter.py
├── wordlists/
│   └── subdomains.txt
├── reports/          ← gerado depois de executar
├── main.py
├── requirements.txt
└── README.md
```

---

## 👨‍💻 Autor

**Henrique** — Estudante de Ciência da Computação | Unisantos  
Desenvolvido como projeto de portfólio para a área de Cibersegurança.