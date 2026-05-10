"""
Proxy Yahoo Finance pour le dashboard Portfolio.
Tourne sur http://localhost:5000 et contourne le blocage CORS.

Dependances : pip install flask requests
"""

from flask import Flask, Response, request
import requests

app = Flask(__name__)

YAHOO_BASE = "https://query1.finance.yahoo.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://finance.yahoo.com/",
}


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


@app.route("/quote/<path:ticker>")
def quote(ticker):
    """Proxy un ticker individuel vers Yahoo Finance v8/finance/chart."""
    params = {
        "interval": request.args.get("interval", "1d"),
        "range":    request.args.get("range", "2d"),
    }
    url = f"{YAHOO_BASE}/v8/finance/chart/{ticker}"
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=12)
        return Response(
            r.content,
            status=r.status_code,
            content_type="application/json; charset=utf-8",
        )
    except requests.exceptions.ConnectionError:
        return Response(
            '{"error":"Impossible de joindre Yahoo Finance. Verifiez votre connexion."}',
            status=503,
            content_type="application/json",
        )
    except Exception as e:
        return Response(
            f'{{"error":"{str(e)}"}}',
            status=500,
            content_type="application/json",
        )


@app.route("/health")
def health():
    return {"status": "ok", "port": 5000}


if __name__ == "__main__":
    print("=" * 55)
    print("  Proxy Yahoo Finance - Portfolio Dashboard")
    print("  http://localhost:5000")
    print("=" * 55)
    print("  Gardez cette fenetre ouverte pendant l'utilisation")
    print("  du dashboard. Fermez-la pour arreter le serveur.")
    print("=" * 55)
    app.run(host="localhost", port=5000, debug=False)
