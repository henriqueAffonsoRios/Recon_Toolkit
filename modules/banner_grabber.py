import socket
from colorama import Fore, Style, init

init(autoreset=True)


def grab_banner(host: str, port: int, timeout: float = 2.0) -> str | None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))

            # Alguns serviços enviam o banner assim que conectamos
            # Outros precisam de uma requisição primeiro — tentamos os dois
            try:
                banner = sock.recv(1024).decode(errors="ignore").strip()
                if banner:
                    return banner
            except socket.timeout:
                pass

            # Se não respondeu, enviamos uma requisição HTTP básica
            # Servidores web respondem a isso com seus headers
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            try:
                banner = sock.recv(1024).decode(errors="ignore").strip()
                if banner:
                    return banner
            except socket.timeout:
                pass

    except (socket.error, ConnectionRefusedError):
        pass

    return None


def run(host: str, portas_abertas: list[dict]) -> list[dict]:
    print(f"\n{Fore.CYAN}[*] Iniciando Banner Grabbing em {host}")

    resultados = []

    for item in portas_abertas:
        porta = item["porta"]
        print(f"  {Fore.YELLOW}[~] Tentando porta {porta}...")

        banner = grab_banner(host, porta)

        if banner:
            # Pega apenas a primeira linha do banner — geralmente é a mais relevante
            primeira_linha = banner.splitlines()[0]
            print(f"  {Fore.GREEN}[+] Porta {porta} → {primeira_linha}")
            resultados.append({"porta": porta, "banner": primeira_linha})
        else:
            print(f"  {Fore.RED}[-] Porta {porta} → Sem banner")
            resultados.append({"porta": porta, "banner": None})

    print(f"{Fore.CYAN}[*] Banner Grabbing concluído.")
    return resultados