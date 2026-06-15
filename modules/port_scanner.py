import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}


def scan_port(host: str, port: int, timeout: float = 1.0) -> dict | None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            resultado = sock.connect_ex((host, port))
            if resultado == 0:
                servico = COMMON_PORTS.get(port, "Desconhecido")
                return {"porta": port, "estado": "aberta", "servico": servico}
    except (socket.timeout, socket.error):
        pass
    return None


def run(host: str, porta_inicio: int = 1, porta_fim: int = 1024) -> list[dict]:
    print(f"\n{Fore.CYAN}[*] Iniciando Port Scan em {host} (portas {porta_inicio}-{porta_fim})")

    portas_abertas = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futuros = {
            executor.submit(scan_port, host, porta): porta
            for porta in range(porta_inicio, porta_fim + 1)
        }
        for futuro in as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                portas_abertas.append(resultado)
                print(f"  {Fore.GREEN}[+] Porta {resultado['porta']:5d}/TCP  aberta  →  {resultado['servico']}")

    portas_abertas.sort(key=lambda x: x["porta"])

    if not portas_abertas:
        print(f"  {Fore.YELLOW}[-] Nenhuma porta aberta encontrada.")

    print(f"{Fore.CYAN}[*] Port Scan concluído. {len(portas_abertas)} porta(s) aberta(s).")
    return portas_abertas