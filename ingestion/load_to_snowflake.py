import json
import os
import snowflake.connector
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()


def upload_json_to_snowflake():
    # Caminho do ficheiro JSON
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "markets.json")

    if not os.path.exists(json_path):
        print("❌ Ficheiro markets.json não encontrado.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Conectar ao Snowflake
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        )
        cursor = conn.cursor()

        # Converte a lista inteira de objetos para uma única string JSON
        json_string = json.dumps(data)

        # Query que faz a explosão do array JSON e insere cada elemento na coluna RAW_PAYLOAD
        insert_query = """
            INSERT INTO BRONZE.RAW_MARKET_DATA (RAW_PAYLOAD)
            SELECT value
            FROM TABLE(FLATTEN(input => PARSE_JSON(%s)));
        """

        cursor.execute(insert_query, (json_string,))
        conn.commit()

        print(
            f"✅ {len(data)} registos inseridos com sucesso na camada BRONZE!"
        )

    except Exception as e:
        print(f"❌ Erro ao carregar dados no Snowflake: {e}")
    finally:
        if "conn" in locals():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    upload_json_to_snowflake()