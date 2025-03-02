# This is an example feature definition file

from datetime import timedelta

from feast import KafkaSource
from feast.data_format import JsonFormat
from feast.infra.offline_stores.contrib.trino_offline_store.trino_source import (
    TrinoSource,
)

loan_batch_source = TrinoSource(
    event_timestamp_column="event_timestamp",
    table_ref="feast.driver_stats",
    created_timestamp_column="created",
)

loan_stream_source = KafkaSource(
    name="device_stats_stream_source",
    kafka_bootstrap_servers="localhost:9092",
    topic="device_0",
    timestamp_field="created",
    batch_source=loan_batch_source,
    message_format=JsonFormat(
        schema_json="created timestamp, device_id integer, feature_5 double, feature_3 double, feature_1 double, feature_8 double, feature_6 double, feature_0 double, feature_4 double"
    ),
    watermark_delay_threshold=timedelta(minutes=1),
)
