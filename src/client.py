import pika
import uuid
import json


class RpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, request):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='SRV.Q',
                                   properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                   correlation_id=self.corr_id),
                                   body=json.dumps(request))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


def test_scenarios():
    client = RpcClient()

    response = client.call({'action': 'add_category', 'name': 'Fruits'})
    print("Add Category:", response)

    response = client.call({'action': 'add_category', 'name': 'Vegetables'})
    print("Add Category:", response)

    response = client.call({'action': 'add_product', 'name': 'Apple', 'price': 1.2, 'category_id': 1})
    print("Add Product:", response)

    response = client.call({'action': 'add_product', 'name': 'Banana', 'price': 0.5, 'category_id': 1})
    print("Add Product:", response)

    response = client.call({'action': 'add_product', 'name': 'Carrot', 'price': 0.8, 'category_id': 2})
    print("Add Product:", response)

    response = client.call({'action': 'edit_category', 'id': 2, 'name': 'Root Vegetables'})
    print("Edit Category:", response)

    response = client.call({'action': 'edit_product', 'id': 3, 'name': 'Baby Carrot', 'price': 0.9, 'category_id': 2})
    print("Edit Product:", response)

    response = client.call({'action': 'search_categories', 'name': 'Root'})
    print("Search Categories:", response)

    response = client.call({'action': 'search_products', 'name': 'Apple'})
    print("Search Products:", response)

    response = client.call({'action': 'delete_product', 'id': 2})
    print("Delete Product:", response)

    response = client.call({'action': 'delete_category', 'id': 1})
    print("Delete Category:", response)


if __name__ == '__main__':
    test_scenarios()
