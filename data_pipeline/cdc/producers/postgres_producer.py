import logging
import os
import fsspec
import pandas as pd

from kafka.producer import KafkaProducer

def postgres_producer():
    producer = KafkaProducer(
        boostrap_servers="my-kafka-cluster-kafka-bootstrap:9092"
    )