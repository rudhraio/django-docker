import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()


import pika
import json
from common.configs.config import config as cfg
from myapp.models import Product, ProductInventory



credentials = pika.PlainCredentials(
    cfg.get("rabbit_mq", "USER_NAME"), cfg.get("rabbit_mq", "PASSWORD")
)
parameters = pika.ConnectionParameters(
    host=cfg.get("rabbit_mq", "HOST"),
    virtual_host=cfg.get("rabbit_mq", "VIRTUAL_HOST"),
    credentials=credentials,
    frame_max=int(cfg.get("rabbit_mq", "FRAME_MAX")),
    heartbeat=int(cfg.get("rabbit_mq", "HEART_BEAT")),
    connection_attempts=int(cfg.get("rabbit_mq", "CONNECTION_ATTEMPTS")),
)


def callback(ch, method, properties, body):
    # Process the received message body
    json_body = json.loads(body)
    action = json_body["action"]
    product_id = json_body["product_id"]
    if action == 'created':
        # Create inventory record for the new product
        product = Product.objects.get(id=product_id)
        ProductInventory.objects.create(product=product)
    elif action == 'updated':
        # Increment inventory count by 10 for the updated product
        product_inventory = ProductInventory.objects.get(product_id=product_id)
        product_inventory.inventory_count += 10
        product_inventory.save()
    else:
        # Handle other actions if needed
        pass
    # You can parse the body to extract product_id and action if needed


# Establish a connection to RabbitMQ using the specified parameters
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the exchange (if not already declared)
channel.exchange_declare(exchange='myprojectexchange', exchange_type='fanout')

# Declare a queue and bind it to the exchange
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='myprojectexchange', queue=queue_name)

# Consume messages from the queue
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

# Start consuming messages
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
