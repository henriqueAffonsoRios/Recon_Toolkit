import requests
from colorama import Fore, init

init(autoreset=True)

# Headers de segurança que vamos verificar e o que cada um faz
SECURITY_HEADERS = {
    "Content-Security-Policy": "Proteção contra XSS e injeção de conteúdo",
    "Strict-Transport-Security": "Força uso de HTTPS (evita downgrade)",
    "X-Frame-Options": "Proteção contra Clickjacking",
    "X-Content-Type-Options": "Proteção contra MIME sniffing",
    "Referrer-Policy": "Controle de informações no header Referer",
    "Permissions-Policy": "Controle de acesso a recursos do navegador",
}


def run(host: str) -> dict:
    print(f"\n{Fore.CYAN}[*] Analisando Security Headers em {host}")

    # Garante que a URL tem o protocolo correto
    url = host if host.startswith("http") else f"http://{host}"

    resultados = {"presentes": {}, "ausentes": []}

    try:
        # verify=False ignora erros de certificado SSL
        # timeout=10 evita travar caso o servidor demore
        # allow_redirects=True segue redirecionamentos (http → https)
        resposta = requests.get(url, timeout=10, verify=False,
                                allow_redirects=True)

        print(f"  {Fore.CYAN}[*] Resposta recebida → "
              f"Status {resposta.status_code} | URL final: {resposta.url}")

        headers_recebidos = resposta.headers

        print(f"\n  {'─' * 55}")

        for header, descricao in SECURITY_HEADERS.items():
            if header in headers_recebidos:
                valor = headers_recebidos[header]
                print(f"  {Fore.GREEN}[+] PRESENTE  {header}")
                print(f"           Valor: {valor[:80]}")
                resultados["presentes"][header] = valor
            else:
                print(f"  {Fore.RED}[-] AUSENTE   {header}")
                print(f"           Risco: {descricao}")
                resultados["ausentes"].append(header)

        print(f"  {'─' * 55}")

        total = len(SECURITY_HEADERS)
        presentes = len(resultados["presentes"])
        ausentes = len(resultados["ausentes"])

        cor_score = Fore.GREEN if presentes >= 4 else Fore.YELLOW if presentes >= 2 else Fore.RED
        print(f"\n  {cor_score}[*] Score: {presentes}/{total} headers de segurança presentes")

    except requests.exceptions.ConnectionError:
        print(f"  {Fore.RED}[!] Não foi possível conectar em {url}")
    except requests.exceptions.Timeout:
        print(f"  {Fore.RED}[!] Timeout ao conectar em {url}")

    print(f"{Fore.CYAN}[*] Análise de headers concluída.")
    return resultados