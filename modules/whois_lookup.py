import whois
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

# Campos que queremos exibir e seus rótulos em português
CAMPOS = {
    "domain_name":  "Domínio",
    "registrar":    "Registrador",
    "creation_date":"Data de criação",
    "expiration_date": "Data de expiração",
    "updated_date": "Última atualização",
    "name_servers": "Nameservers",
    "emails":       "E-mails de contato",
    "org":          "Organização",
    "country":      "País",
}


def formatar_valor(valor) -> str:
    """
    O python-whois às vezes retorna listas ao invés de strings.
    Essa função normaliza o valor para exibição.
    """
    if isinstance(valor, list):
        # Remove duplicatas mantendo a ordem e pega os 3 primeiros
        vistos = []
        for item in valor:
            item_str = str(item).strip()
            if item_str not in vistos:
                vistos.append(item_str)
        return "\n              ".join(vistos[:3])

    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y %H:%M")

    return str(valor).strip()


def run(dominio: str) -> dict:
    print(f"\n{Fore.CYAN}[*] Iniciando WHOIS Lookup em {dominio}")

    resultados = {}

    try:
        dados = whois.whois(dominio)

        print(f"  {'─' * 55}")

        for campo, rotulo in CAMPOS.items():
            valor = getattr(dados, campo, None)

            if valor:
                valor_formatado = formatar_valor(valor)
                print(f"  {Fore.GREEN}[+] {rotulo:<22} {valor_formatado}")
                resultados[campo] = str(valor)
            else:
                print(f"  {Fore.YELLOW}[-] {rotulo:<22} Não disponível")

        print(f"  {'─' * 55}")

    except Exception as e:
        print(f"  {Fore.RED}[!] Erro ao consultar WHOIS: {e}")

    print(f"{Fore.CYAN}[*] WHOIS Lookup concluído.")
    return resultados