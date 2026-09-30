{{ config(materialized='table') }}

WITH raw_source AS (
    SELECT 
        RAW_PAYLOAD,
        INGESTED_AT
    FROM {{ source('bronze_data', 'RAW_MARKET_DATA') }}
)

SELECT
    RAW_PAYLOAD:id::STRING AS coin_id,
    RAW_PAYLOAD:symbol::STRING AS symbol,
    RAW_PAYLOAD:name::STRING AS coin_name,
    RAW_PAYLOAD:current_price::FLOAT AS current_price_usd,
    RAW_PAYLOAD:market_cap::NUMBER AS market_cap_usd,
    RAW_PAYLOAD:market_cap_rank::INT AS market_cap_rank,
    RAW_PAYLOAD:total_volume::FLOAT AS total_volume,
    RAW_PAYLOAD:high_24h::FLOAT AS high_24h,
    RAW_PAYLOAD:low_24h::FLOAT AS low_24h,
    RAW_PAYLOAD:price_change_percentage_24h::FLOAT AS price_change_pct_24h,
    RAW_PAYLOAD:last_updated::TIMESTAMP_NTZ AS api_last_updated,
    INGESTED_AT AS ingested_at
FROM raw_source