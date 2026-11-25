"""30 evaluation questions: 20 with an answer in the corpus, 10 without.

For answerable questions, `doc` is the slug of the document that should answer it
(the gold source). For unanswerable ones, `doc` is None — the assistant should
say it couldn't find anything rather than invent an answer.
"""

QUESTIONS = [
    # ---- answerable (gold document slug) --------------------------------------
    dict(q="How do I install Northwind CLI?", doc="install"),
    dict(q="What Python version does Northwind need?", doc="install"),
    dict(q="How do I start a new project?", doc="quickstart"),
    dict(q="What are the top-level sections of northwind.yaml?", doc="config"),
    dict(q="What role does the Postgres connector use when it is a source?", doc="connectors-postgres"),
    dict(q="What file format is recommended in S3 for large data?", doc="connectors-s3"),
    dict(q="Is BigQuery a source or a destination?", doc="connectors-bigquery"),
    dict(q="Does Northwind include its own scheduler?", doc="scheduling"),
    dict(q="How many times is a failed step retried?", doc="retries"),
    dict(q="How do I get logs in JSON format?", doc="logging"),
    dict(q="Where are secrets stored?", doc="secrets"),
    dict(q="What does nw run --dry-run do?", doc="commands-run"),
    dict(q="What does nw validate check?", doc="commands-validate"),
    dict(q="How does backfill handle a failure mid-range?", doc="commands-backfill"),
    dict(q="What kind of SQL statement must a transform be?", doc="transforms"),
    dict(q="What can nw test assertions check?", doc="testing"),
    dict(q="What is the recommended way to deploy Northwind?", doc="deployment"),
    dict(q="What does the connector do when an API returns HTTP 429?", doc="rate-limits"),
    dict(q="What does a 'config invalid' error mean?", doc="troubleshooting"),
    dict(q="How do I pin the version in production?", doc="upgrade"),

    # ---- unanswerable (not in the corpus) -------------------------------------
    dict(q="What is the refund policy?", doc=None),
    dict(q="Does Northwind have a mobile app?", doc=None),
    dict(q="Who founded the Northwind company?", doc=None),
    dict(q="How much does the Enterprise plan cost?", doc=None),
    dict(q="Does Northwind support Kafka as a source?", doc=None),
    dict(q="What is the uptime SLA for Northwind cloud?", doc=None),
    dict(q="Does Northwind integrate with Salesforce?", doc=None),
    dict(q="What is the phone number for support?", doc=None),
    dict(q="Does Northwind offer a free trial?", doc=None),
    dict(q="How do I change the UI theme?", doc=None),
]
