import dns.resolver
import random
import string
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)


def detectar_wildcard(dominio: str) -> str | None:
    """
    Testa um subdomínio aleatório para detectar wildcard DNS.
    Se resolver, retorna o IP do wildcard para filtrarmos depois.
    Se não resolver, o domínio não tem wildcard.
    """
    subdominio_aleatorio = ''.join(random.choices(string.ascii_lowercase, k=12))
    teste = f"{subdominio_aleatorio}.{dominio}"
    try:
        respostas = dns.resolver.resolve(teste, "A")
        return str(respostas[0])
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
            dns.resolver.NoNameservers, dns.exception.Timeout):
        return None


def testar_subdominio(subdominio: str) -> dict | None:
    try:
        respostas = dns.resolver.resolve(subdominio, "A")
        ips = [str(r) for r in respostas]
        return {"subdominio": subdominio, "ips": ips}
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,
            dns.resolver.NoNameservers, dns.exception.Timeout):
        return None


def carregar_wordlist(caminho: str) -> list[str]:
    try:
        with open(caminho, "r") as f:
            return [
                linha.strip()
                for linha in f
                if linha.strip() and not linha.startswith("#")
            ]
    except FileNotFoundError:
        print(f"  {Fore.RED}[!] Wordlist não encontrada em: {caminho}")
        return []


def run(dominio: str, wordlist_path: str = "wordlist/subdomains.txt") -> list[dict]:
    print(f"\n{Fore.CYAN}[*] Iniciando Subdomain Enumeration em {dominio}")

    # Detecta wildcard antes de começar
    ip_wildcard = detectar_wildcard(dominio)
    if ip_wildcard:
        print(f"  {Fore.YELLOW}[!] Wildcard DNS detectado → qualquer subdomínio "
              f"resolve para {ip_wildcard}")
        print(f"  {Fore.YELLOW}[!] Resultados com esse IP serão marcados como suspeitos.")

    palavras = carregar_wordlist(wordlist_path)
    if not palavras:
        return []

    print(f"  {Fore.CYAN}[*] Testando {len(palavras)} subdomínios possíveis...")

    encontrados = []
    subdominios = [f"{palavra}.{dominio}" for palavra in palavras]

    with ThreadPoolExecutor(max_workers=30) as executor:
        futuros = {
            executor.submit(testar_subdominio, sub): sub
            for sub in subdominios
        }
        for futuro in as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                # Verifica se o IP é o mesmo do wildcard
                suspeito = ip_wildcard and ip_wildcard in resultado["ips"]
                status = "SUSPEITO" if suspeito else "VÁLIDO"
                cor = Fore.YELLOW if suspeito else Fore.GREEN

                encontrados.append({**resultado, "status": status})
                print(f"  {cor}[+] {resultado['subdominio']} "
                      f"→ {', '.join(resultado['ips'])} [{status}]")

    validos = [r for r in encontrados if r["status"] == "VÁLIDO"]

    print(f"{Fore.CYAN}[*] Concluído. {len(encontrados)} encontrado(s), "
          f"{len(validos)} válido(s).")

    return encontrados