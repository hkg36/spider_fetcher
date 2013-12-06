from kombu import Connection
from kombu import Exchange, Queue
import config
connection = Connection(hostname=config.Queue_Server,
                        port=config.Queue_Port,
                        userid=config.Queue_User,
                        password=config.Queue_PassWord,
                        virtual_host=config.Queue_Path)
channel = connection.channel()
task_queue = Queue('net_request',durable=True,channel=channel)
task_queue.delete()

task_queue = Queue('weibo_request',durable=True,channel=channel)
task_queue.delete()

connection.close()
