import os
from datetime import datetime, timedelta, timezone

import dlt
from dotenv import load_dotenv
from logfire.query_client import LogfireQueryClient

load_dotenv()

client = LogfireQueryClient(read_token=os.environ["LOGFIRE_READ_TOKEN"])

sql = """
SELECT *
FROM records
ORDER BY start_timestamp DESC
"""

# Logfire now recommends providing a minimum timestamp.
min_ts = datetime.now(timezone.utc) - timedelta(days=30)

result = client.query_json_rows(
    sql,
    min_timestamp=min_ts,
    limit=10_000,
)

columns = [c["name"] for c in result["columns"]]
rows = [
    dict(zip(columns, row, strict=False))
    for row in result["rows"]
]



pipeline = dlt.pipeline(
    pipeline_name="logfire",
    destination=dlt.destinations.duckdb("logfire.duckdb"),
    dataset_name="raw",
)

info = pipeline.run(
    rows,
    table_name="records",
    write_disposition="replace",
)

print(info)