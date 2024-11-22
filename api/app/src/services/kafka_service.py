import asyncio
import json
import os
from datetime import datetime
from confluent_kafka import Producer
from threading import Thread

conf = {'bootstrap.servers': f'{os.getenv("KAFKA_HOST")}:{os.getenv("KAFKA_PORT")}'}

class AIOProducer:
    def __init__(self, config, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._producer = Producer(config)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic, value):
        result = self._loop.create_future()
        self._producer.produce(topic, value)
        return result


aio_producer = AIOProducer(conf)

def send_message_to_kafka_topic(topic_name, message):
    aio_producer.produce(topic_name, json.dumps(message))

def get_kafka_message(rate_id, date, cargo_type, rate, user_id, event_type):
    message = {
        "user_id": user_id,
        "event_type": event_type,
        "event_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "rate_id": rate_id,
        "date": date.strftime('%Y-%m-%d'),
        "cargo_type": cargo_type,
        "rate": rate,
    }
    return message

def send_update_rate_message_to_kafka(rate_id, date, cargo_type, rate, user_id):
    message = get_kafka_message(rate_id, date, cargo_type, rate, user_id, "update")
    send_message_to_kafka_topic('update_logger', message)


def send_delete_rate_message_to_kafka(rate_id, date, cargo_type, rate, user_id):
    message = get_kafka_message(rate_id, date, cargo_type, rate, user_id, "delete")
    send_message_to_kafka_topic('delete_logger', message)