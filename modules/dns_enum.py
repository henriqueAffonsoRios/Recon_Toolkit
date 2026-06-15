import dns.resolver
from colorama import Fore, init

init(autoreset=True)

TIPOS_REGISTRO = ["A", "MX", "NS", "TXT", "CNAME"]


def consultar_registro(dominio: str, tipo: str) -> list[str]:
    """
    Consulta um tipo específico de registro DNS para o domínio.
    Retorna lista de resultados ou lista vazia se não encontrar.
    """
    try:
        respostas = dns.resolver.resolve(dominio, tipo)
        return [str(r) for r in respostas]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers, dns.exception.Timeout):
        return []


def run(dominio: str) -> dict:
    print(f"\n{Fore.CYAN}[*] Iniciando DNS Enumeration em {dominio}")

    resultados = {}

    for tipo in TIPOS_REGISTRO:
        registros = consultar_registro(dominio, tipo)

        if registros:
            print(f"\n  {Fore.GREEN}[+] Registros {tipo}:")
            for registro in registros:
                print(f"      → {registro}")
            resultados[tipo] = registros
        else:
            print(f"  {Fore.RED}[-] Sem registros {tipo}")
            resultados[tipo] = []

    print(f"\n{Fore.CYAN}[*] DNS Enumeration concluída.")
    return resultados