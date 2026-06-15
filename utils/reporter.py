import json
import os
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)


def gerar_relatorio(alvo: str, resultados: dict, pasta_saida: str = "reports") -> dict:
    """
    Recebe todos os resultados dos módulos e gera dois arquivos:
    - report_<alvo>_<timestamp>.json  → dados estruturados
    - report_<alvo>_<timestamp>.txt   → resumo legível
    """

    # Cria a pasta de reports se não existir
    os.makedirs(pasta_saida, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Remove caracteres inválidos para nome de arquivo
    alvo_limpo = alvo.replace(".", "_").replace(":", "_")
    nome_base = f"report_{alvo_limpo}_{timestamp}"

    caminho_json = os.path.join(pasta_saida, f"{nome_base}.json")
    caminho_txt = os.path.join(pasta_saida, f"{nome_base}.txt")

    # Estrutura completa do relatório
    relatorio = {
        "meta": {
            "alvo": alvo,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "ferramenta": "Recon Toolkit v1.0",
        },
        "resultados": resultados
    }

    # Salva JSON
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=4, default=str)

    # Salva TXT
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("         RECON TOOLKIT — RELATÓRIO DE RECONHECIMENTO\n")
        f.write("=" * 60 + "\n")
        f.write(f"Alvo    : {alvo}\n")
        f.write(f"Data    : {relatorio['meta']['data']}\n")
        f.write("=" * 60 + "\n\n")

        # Portas abertas
        f.write("[1] PORT SCAN\n")
        f.write("-" * 40 + "\n")
        portas = resultados.get("port_scan", [])
        if portas:
            for p in portas:
                f.write(f"  Porta {p['porta']:5}/TCP  →  {p['servico']}\n")
        else:
            f.write("  Nenhuma porta encontrada.\n")
        f.write("\n")

        # Banners
        f.write("[2] BANNER GRABBING\n")
        f.write("-" * 40 + "\n")
        banners = resultados.get("banner_grabbing", [])
        if banners:
            for b in banners:
                banner = b.get("banner") or "Sem banner"
                f.write(f"  Porta {b['porta']:5}  →  {banner}\n")
        else:
            f.write("  Nenhum banner coletado.\n")
        f.write("\n")

        # DNS
        f.write("[3] DNS ENUMERATION\n")
        f.write("-" * 40 + "\n")
        dns = resultados.get("dns_enum", {})
        if dns:
            for tipo, registros in dns.items():
                if registros:
                    f.write(f"  {tipo}:\n")
                    for r in registros:
                        f.write(f"    → {r}\n")
        else:
            f.write("  Nenhum registro encontrado.\n")
        f.write("\n")

        # Subdomínios
        f.write("[4] SUBDOMAIN ENUMERATION\n")
        f.write("-" * 40 + "\n")
        subs = resultados.get("subdomain_enum", [])
        validos = [s for s in subs if s.get("status") == "VÁLIDO"]
        suspeitos = [s for s in subs if s.get("status") == "SUSPEITO"]
        if validos:
            for s in validos:
                f.write(f"  [VÁLIDO]   {s['subdominio']} → {', '.join(s['ips'])}\n")
        if suspeitos:
            f.write(f"  [SUSPEITO] {len(suspeitos)} subdomínio(s) — possível wildcard DNS\n")
        if not subs:
            f.write("  Nenhum subdomínio encontrado.\n")
        f.write("\n")

        # HTTP Headers
        f.write("[5] HTTP SECURITY HEADERS\n")
        f.write("-" * 40 + "\n")
        headers = resultados.get("http_headers", {})
        presentes = headers.get("presentes", {})
        ausentes = headers.get("ausentes", [])
        if presentes:
            f.write("  Presentes:\n")
            for h in presentes:
                f.write(f"    ✓ {h}\n")
        if ausentes:
            f.write("  Ausentes:\n")
            for h in ausentes:
                f.write(f"    ✗ {h}\n")
        f.write(f"  Score: {len(presentes)}/{len(presentes) + len(ausentes)}\n\n")

        # WHOIS
        f.write("[6] WHOIS LOOKUP\n")
        f.write("-" * 40 + "\n")
        whois = resultados.get("whois_lookup", {})
        campos = {
            "registrar": "Registrador",
            "creation_date": "Criação",
            "expiration_date": "Expiração",
            "org": "Organização",
            "country": "País"
        }
        if whois:
            for campo, rotulo in campos.items():
                if campo in whois:
                    f.write(f"  {rotulo:<16} {str(whois[campo])[:60]}\n")
        else:
            f.write("  Dados não disponíveis.\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("                    FIM DO RELATÓRIO\n")
        f.write("=" * 60 + "\n")

    print(f"\n{Fore.GREEN}[+] Relatório JSON salvo em: {caminho_json}")
    print(f"{Fore.GREEN}[+] Relatório TXT  salvo em: {caminho_txt}")

    return {"json": caminho_json, "txt": caminho_txt}