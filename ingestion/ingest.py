import json
import os
import requests

# URL pública da API do CoinGecko (Top 100 moedas por Market Cap)
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1"


def fetch_crypto_data():
    """Faz a requisição para a API do CoinGecko e retorna o JSON."""
    try:
        response = requests.get(COINGECKO_URL, timeout=10)
        response.raise_for_status()
        print("✅ Dados extraídos da API CoinGecko com sucesso!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar com a API: {e}")
        return None


def save_json_locally(data, filename="markets.json"):
    """Salva os dados extraídos em um arquivo JSON na pasta de ingestão."""
    if not data:
        print("⚠️ Nenhum dado para salvar.")
        return

    # Garante o caminho relativo correto dentro da pasta 'ingestion'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"💾 Arquivo salvo com sucesso em: {output_path}")


if __name__ == "__main__":
    market_data = fetch_crypto_data()
    save_json_locally(market_data)