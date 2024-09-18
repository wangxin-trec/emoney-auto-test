import threading
from esdbclient import EventStoreDBClient, NewEvent
from uuid import uuid4
from esdbclient.streams import StreamState
from util.Logger import logger

# 定义节点 URI
client_uris = [
    "esdb+discover://10.0.2.6:2113?tls=false&tlsVerifyCert=false",
    "esdb+discover://10.0.2.7:2113?tls=false&tlsVerifyCert=false",
    "esdb+discover://10.0.2.8:2113?tls=false&tlsVerifyCert=false"
]

# 创建客户端连接，放入 try-catch
def create_clients():
    clients = []
    for i, uri in enumerate(client_uris, start=1):
        try:
            client = EventStoreDBClient(uri=uri)
            clients.append(client)
            logger.info(f'[OK] Connected to client_node{i} with URI: {uri}')
        except Exception as e:
            logger.error(f'ERROR: Failed to connect to client_node{i} with URI: {uri}, Error: ' + str(e))
            clients.append(None)  # 即使连接失败，也保持索引一致性
    return clients

clients = create_clients()

# 通用的写入函数
def write_data_to_client(client, node_name):
    if client is None:
        logger.error(f'SKIP: Write ESDB event for {node_name}, client is None')
        return
    try:
        logger.info(f'Begin: Write ESDB event for {node_name} ----------------->')
        new_event = NewEvent(
            id=uuid4(),
            type="TestEvent",
            data=b"I wrote my first event",
        )
        client.append_to_stream(
            "some-stream",
            events=[new_event],
            current_version=StreamState.ANY,
        )
        logger.info(f'[OK] End: Write ESDB event for {node_name} <-----------------')
    except Exception as e:
        logger.error(f'ERROR: Write ESDB event for {node_name}: ' + str(e))

# 通用的读取函数
def read_data_from_client(client, node_name):
    if client is None:
        logger.error(f'SKIP: Read ESDB event for {node_name}, client is None')
        return
    try:
        logger.info(f'Begin: Read ESDB event for {node_name} ----------------->')
        events = client.get_stream("some-stream")
        for event in events:
            logger.info(f'{node_name} ---> ' + str(event))
        logger.info(f'[OK] End: Read ESDB event for {node_name} <-----------------')
    except Exception as e:
        logger.error(f'ERROR: Read ESDB event for {node_name}: ' + str(e))

# 多线程写入数据
def test_write_data():
    threads = []
    for i, client in enumerate(clients, start=1):
        node_name = f'client_node{i}'
        t = threading.Thread(target=write_data_to_client, args=(client, node_name))
        t.start()
        threads.append(t)
    
    # 等待所有线程执行完毕
    for t in threads:
        t.join()

# 多线程读取数据
def test_read_data():
    threads = []
    for i, client in enumerate(clients, start=1):
        node_name = f'client_node{i}'
        t = threading.Thread(target=read_data_from_client, args=(client, node_name))
        t.start()
        threads.append(t)
    
    # 等待所有线程执行完毕
    for t in threads:
        t.join()

if __name__ == '__main__':
    test_write_data()
    test_read_data()
