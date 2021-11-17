import config as CONFIG

from flask import Flask
from utils import run_io_tasks_in_parallel, publish_data, feedUrl, recieve_data


app = Flask(__name__)

@app.route('/')
def execute_publisher():
    """Resource to execute publisher"""
    file_exp = 'export.xml'
    file_mall = 'mall.xml'
    filter_tag = 'HEUREKA_CPC'

    print('>> Running publisher..')
    run_io_tasks_in_parallel([
        lambda: feedUrl(CONFIG.URL1, file_exp),
        lambda: feedUrl(CONFIG.URL2, file_mall),
    ])
    run_io_tasks_in_parallel([
        lambda: publish_data(CONFIG.QUEUE_SHOP_ITEMS, CONFIG.QUEUE_SHOP_ITEMS, local_file=file_exp),
        # lambda: publish_data(CONFIG.QUEUE_SHOP_ITEMS, CONFIG.QUEUE_SHOP_ITEMS, local_file=file_mall),
        lambda: publish_data(CONFIG.QUEUE_SHOP_BID, CONFIG.QUEUE_SHOP_BID, filter_tag=filter_tag, local_file=file_exp),
        # lambda: publish_data(CONFIG.QUEUE_SHOP_BID, CONFIG.QUEUE_SHOP_BID, filter_tag=filter_tag, local_file=file_mall),
    ])
    return 'Done publishing data'


@app.route('/reciever')
def execute_reciever():
    """Resource to execute reciever"""
    print('>> Running reciever..')
    recieve_data()