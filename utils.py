import pika
import requests
import shutil
import config as CONFIG
import xml.etree.ElementTree as ET

from concurrent.futures import ThreadPoolExecutor


def parse_xml(file_path, tag, file_name='output.xml'):
    """Get queue connection"""
    try:
        print('chosen file {}'.format(file_name))
        root = ET.parse(file_path).getroot()
        for child in root:
            filtered_tags = [elem.tag for elem in child.iter() if elem.tag == tag] if tag else []
            if not filtered_tags:
                root.remove(child)

        tree = ET.ElementTree(root)
        print('starts writing')
        tree.write(file_name)
        print('done writing')
        return True
    except Exception as exc:
        raise 'Failed to parse xml. err: {}'.format(exc)


def feedUrl(url, local_filename):
    """Feed xml data"""
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def run_io_tasks_in_parallel(tasks):
    """Execute tasks in parallel"""
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


def get_connection():
    """Get queue connection"""
    try:
        credentials = pika.PlainCredentials(CONFIG.USER, CONFIG.PASSWORD)
        parameters = pika.ConnectionParameters(
            CONFIG.HOST, CONFIG.PORT, '/', credentials)
        return pika.BlockingConnection(parameters)
    except Exception as exc:
        raise ConnectionError('Failed to setup connection. err: {}'.format(exc))


def publish_data(queue, route_key, filter_tag=None, local_file=None):
    """Publish data to queue"""
    if filter_tag and local_file:
        file_name = '{}_{}.xml'.format(local_file, queue)
        parse_xml(local_file, filter_tag, file_name=file_name)

    with open(local_file, 'r', encoding='ISO-8859–1') as fp:
        lines = fp.readlines()

    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    print('Sending data {} to queue {}'.format(route_key, queue))
    channel.basic_publish('', route_key, ''.join(lines))  # async
    connection.close()
    print("Feed {} was sent to queue {}".format(local_file, queue))


def recieve_data():
    """Recieve data from queue"""
    def callback(ch, method, properties, body):
        print(">> Received message body {}".format('body'))
    connection = get_connection()
    channel = connection.channel()
    queue = CONFIG.QUEUE_SHOP_BID
    channel.basic_consume(queue=queue,
                      auto_ack=True,
                      on_message_callback=callback)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()