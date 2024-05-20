import pika
import json
from category import add_category, edit_category, delete_category, search_categories
from product import add_product, edit_product, delete_product, search_products


def handle_request(request):
    try:
        data = json.loads(request)
        action = data['action']

        if action == 'add_category':
            add_category(data['name'])
            return {'status': 'success', 'message': 'Category added'}

        elif action == 'edit_category':
            edit_category(data['id'], data['name'])
            return {'status': 'success', 'message': 'Category edited'}

        elif action == 'delete_category':
            delete_category(data['id'])
            return {'status': 'success', 'message': 'Category deleted'}

        elif action == 'search_categories':
            result = search_categories(data.get('name'))
            return {'status': 'success', 'data': result}

        elif action == 'add_product':
            add_product(data['name'], data['price'], data['category_id'])
            return {'status': 'success', 'message': 'Product added'}

        elif action == 'edit_product':
            edit_product(data['id'], data['name'], data['price'], data['category_id'])
            return {'status': 'success', 'message': 'Product edited'}

        elif action == 'delete_product':
            delete_product(data['id'])
            return {'status': 'success', 'message': 'Product deleted'}

        elif action == 'search_products':
            result = search_products(data.get('name'), data.get('category_id'), data.get('price_range'))
            return {'status': 'success', 'data': result}

        else:
            return {'status': 'error', 'message': 'Invalid action'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def on_request(ch, method, props, body):
    response = handle_request(body)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_server():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='SRV.Q')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='SRV.Q', on_message_callback=on_request)

    print("Server started and awaiting requests...")
    channel.start_consuming()


if __name__ == '__main__':
    start_server()
