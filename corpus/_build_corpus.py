"""Write the synthetic corpus: ~18 short docs about a fictional tool, Northwind
CLI (an invented open-source data-pipeline tool). All content is made up, so
there's no copyright or scraping involved, and the facts are specific enough that
the eval can check answers against the source.

Run once: python corpus/_build_corpus.py
"""
from pathlib import Path

HERE = Path(__file__).parent

# (slug, title, source_url, body)
DOCS = [
    ("install", "Installing Northwind CLI",
     "https://docs.northwind.example/install",
     "Northwind CLI needs Python 3.10 or newer. Install it with `pip install northwind-cli`. "
     "On macOS and Linux the binary is placed on your PATH as `nw`. Verify the install by running "
     "`nw --version`. Windows is supported through WSL only; native Windows is not supported."),
    ("quickstart", "Quickstart",
     "https://docs.northwind.example/quickstart",
     "Create a project with `nw init my-pipeline`, which writes a starter `northwind.yaml`. "
     "Add a source and a destination to that file, then run `nw run` to execute the pipeline once. "
     "A first run over the sample data usually finishes in under ten seconds. Use `nw run --watch` to "
     "re-run automatically when the config changes."),
    ("config", "The northwind.yaml config file",
     "https://docs.northwind.example/config",
     "Every project is driven by a single `northwind.yaml` file at the project root. It has three "
     "top-level sections: `sources`, `transforms`, and `destinations`. Environment variables are "
     "referenced with the `${VAR}` syntax and resolved at run time. The file is validated before every "
     "run; an invalid file stops the run before any data moves."),
    ("connectors-postgres", "Postgres connector",
     "https://docs.northwind.example/connectors/postgres",
     "The Postgres connector works as both a source and a destination. Connections use a read-only role "
     "when Postgres is a source, and the connector never issues DDL against a source database. Set the "
     "connection string in `${NW_POSTGRES_URL}`. Batched writes default to 5,000 rows per statement."),
    ("connectors-s3", "S3 connector",
     "https://docs.northwind.example/connectors/s3",
     "The S3 connector reads and writes CSV, JSON, and Parquet. Parquet is recommended for anything over "
     "one million rows because it is far smaller and faster to scan. Credentials come from the standard "
     "AWS environment variables or an instance role. Objects are written under a `date=YYYY-MM-DD` prefix "
     "by default so downstream tools can partition by day."),
    ("connectors-bigquery", "BigQuery connector",
     "https://docs.northwind.example/connectors/bigquery",
     "The BigQuery connector is a destination only. It loads data through staged files rather than "
     "streaming inserts, which keeps costs low for large loads. A load job that fails midway is rolled "
     "back, so a table is never left half-written. Set the dataset with the `dataset` key on the "
     "destination."),
    ("scheduling", "Scheduling pipelines",
     "https://docs.northwind.example/scheduling",
     "Northwind CLI does not run a scheduler of its own. Instead, `nw run` is designed to be called by "
     "cron, Airflow, or any external scheduler. Each run is independent and writes a run record to the "
     "state directory. Use `nw run --since LAST` to process only data added after the previous "
     "successful run."),
    ("retries", "Retries and failure handling",
     "https://docs.northwind.example/retries",
     "A failed step is retried up to three times by default, with exponential backoff starting at two "
     "seconds. Retries apply only to transient errors such as network timeouts; a schema mismatch fails "
     "immediately and is not retried. Set `retries: 0` on a step to disable retries for that step. The "
     "exit code is non-zero if any step fails after its retries are exhausted."),
    ("logging", "Logging",
     "https://docs.northwind.example/logging",
     "Logs are written to stderr in plain text by default, or as JSON when `--log-format json` is set. "
     "The log level is controlled by `--log-level`, which accepts debug, info, warning, and error. Each "
     "log line carries the run id so logs from concurrent runs can be told apart. Northwind CLI never "
     "logs the values of secrets."),
    ("secrets", "Managing secrets",
     "https://docs.northwind.example/secrets",
     "Secrets are never stored in `northwind.yaml`; the file holds only `${VAR}` references. At run time "
     "the values are read from environment variables or a `.env` file in the project root. A `.env` file "
     "should be listed in `.gitignore` and never committed. Northwind CLI redacts anything that looks "
     "like a key from its logs and error messages."),
    ("commands-run", "The run command",
     "https://docs.northwind.example/commands/run",
     "`nw run` executes the whole pipeline once, in the order sources, transforms, destinations. Add "
     "`--dry-run` to validate and plan without writing to any destination. Add `--only STEP` to run a "
     "single named step. The command returns exit code 0 on success and 1 if any step fails."),
    ("commands-validate", "The validate command",
     "https://docs.northwind.example/commands/validate",
     "`nw validate` checks `northwind.yaml` for schema errors, unknown keys, and unresolved `${VAR}` "
     "references without moving any data. It is safe to run in CI on every pull request. The command "
     "exits non-zero when the config is invalid, which makes it a useful pre-merge gate."),
    ("commands-backfill", "The backfill command",
     "https://docs.northwind.example/commands/backfill",
     "`nw backfill --from 2026-01-01 --to 2026-01-31` reprocesses a historical date range. Backfill runs "
     "in daily chunks so a failure part way through only loses the current day, not the whole range. "
     "Backfill writes to the same destinations as a normal run; point it at a staging destination first "
     "if you want to check the output."),
    ("transforms", "Writing transforms",
     "https://docs.northwind.example/transforms",
     "Transforms are SQL files referenced from the `transforms` section and run against the in-memory "
     "engine between source and destination. Each transform must be a single `SELECT`; statements that "
     "modify data are rejected. Transforms can reference the output of earlier transforms by name, which "
     "lets you build a small chain of steps."),
    ("testing", "Testing a pipeline",
     "https://docs.northwind.example/testing",
     "`nw test` runs the assertions defined in the `tests` block against a sample of the output. An "
     "assertion can check row counts, non-null columns, or uniqueness of a key. Failing assertions return "
     "a non-zero exit code so `nw test` fits into CI. Tests run against sampled data, not the full "
     "dataset, so they are fast but not exhaustive."),
    ("deployment", "Deploying Northwind CLI",
     "https://docs.northwind.example/deployment",
     "The recommended deployment is a small container that runs `nw run` on a schedule from an external "
     "scheduler. The state directory must be on persistent storage so incremental runs work across "
     "restarts. A single run is single-process and does not need more than one CPU for typical "
     "workloads. Scale by running independent pipelines rather than threading a single one."),
    ("rate-limits", "Source rate limits",
     "https://docs.northwind.example/rate-limits",
     "When a source is an HTTP API, Northwind CLI respects a `rate_limit` key given in requests per "
     "second. If the API returns HTTP 429, the connector waits for the interval in the `Retry-After` "
     "header before trying again. There is no global rate limit across pipelines; each run is limited on "
     "its own."),
    ("troubleshooting", "Troubleshooting common errors",
     "https://docs.northwind.example/troubleshooting",
     "A run that stops with `config invalid` means `northwind.yaml` failed validation; run `nw validate` "
     "to see the exact line. A `connection refused` error from a source usually means the connection "
     "string or a firewall rule is wrong. If a run hangs, check whether a source API is rate limiting it. "
     "Raising the log level to debug shows the step that is stuck."),
    ("upgrade", "Upgrading and versioning",
     "https://docs.northwind.example/upgrade",
     "Upgrade with `pip install --upgrade northwind-cli`. Northwind CLI follows semantic versioning, so a "
     "minor upgrade never breaks an existing `northwind.yaml`. A major upgrade may change the config "
     "format, and the release notes list a migration command when one is needed. Pin the version in "
     "production with `northwind-cli==MAJOR.MINOR.PATCH`."),
]


def main() -> None:
    for slug, title, source, body in DOCS:
        text = f"---\ntitle: {title}\nsource: {source}\n---\n\n# {title}\n\n{body}\n"
        (HERE / f"{slug}.md").write_text(text)
    print(f"wrote {len(DOCS)} docs to {HERE}")


if __name__ == "__main__":
    main()
