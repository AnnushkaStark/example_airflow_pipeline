from textwrap import dedent

init_query = dedent("""
                CREATE TABLE IF NOT EXISTS currency_rates (
                    currency_code String,
                    rate Float64,
                    api_timestamp DateTime,
                    ingestion_time DateTime DEFAULT now()
                )
                ENGINE = ReplacingMergeTree(api_timestamp)
                ORDER BY (currency_code, api_timestamp)
                TTL ingestion_time + INTERVAL 1 YEAR;
            """).strip()
