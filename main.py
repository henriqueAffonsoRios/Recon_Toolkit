import argparse
import urllib3
from colorama import Fore, init

from modules import port_scanner, banner_grabber, dns_enum
from modules import subdomain_enum, http_headers, whois_lookup
from utils import reporter

# Suprime avisos de SSL (verify=False no http_headers)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

BANNER = f"""
{Fore.RED}
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
{Fore.YELLOW}         T O O L K I T  v1.0
{Fore.WHITE}    Ferramenta educacional de reconhecimento
  Use apenas em sistemas com autorização explícita
"""


def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="Recon Toolkit — Ferramenta educacional de reconhecimento"
    )
    parser.add_argument("--target",   required=True,  help="Alvo (domínio ou IP)")
    parser.add_argument("--ports",    default="1-1024", help="Range de portas (padrão: 1-1024)")
    parser.add_argument("--wordlist", default="wordlist/subdomains.txt",
                        help="Caminho da wordlist para subdomínios")

    args = parser.parse_args()
    alvo = args.target

    # Processa range de portas
    try:
        inicio, fim = map(int, args.ports.split("-"))
    except ValueError:
        print(f"{Fore.RED}[!] Formato de portas inválido. Use: --ports 1-1024")
        return

    print(f"{Fore.CYAN}[*] Alvo: {alvo}")
    print(f"{Fore.CYAN}[*] Portas: {inicio}-{fim}")
    print(f"{Fore.CYAN}{'=' * 55}")

    resultados = {}

    # Módulo 1 — Port Scanner
    resultados["port_scan"] = port_scanner.run(alvo, inicio, fim)

    # Módulo 2 — Banner Grabbing (usa portas abertas do módulo anterior)
    resultados["banner_grabbing"] = banner_grabber.run(alvo, resultados["port_scan"])

    # Módulo 3 — DNS Enumeration
    resultados["dns_enum"] = dns_enum.run(alvo)

    # Módulo 4 — Subdomain Enumeration
    resultados["subdomain_enum"] = subdomain_enum.run(alvo, args.wordlist)

    # Módulo 5 — HTTP Security Headers
    resultados["http_headers"] = http_headers.run(alvo)

    # Módulo 6 — WHOIS Lookup
    resultados["whois_lookup"] = whois_lookup.run(alvo)

    # Gera relatório final
    print(f"\n{Fore.CYAN}{'=' * 55}")
    print(f"{Fore.CYAN}[*] Gerando relatório final...")
    reporter.gerar_relatorio(alvo, resultados)

    print(f"\n{Fore.GREEN}[*] Reconhecimento concluído.")


if __name__ == "__main__":
    main()