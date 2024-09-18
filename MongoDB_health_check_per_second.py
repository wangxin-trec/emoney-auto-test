from pymongo import MongoClient
from util.Logger import logger
import time

def check_mongodb_connection(host, port, username, password, auth_db):
    try:
        # 创建MongoDB客户端
        client = MongoClient(host=host, port=port, username=username, password=password, authSource=auth_db)
        
        # 尝试从"admin"数据库中列出集合名称，以检查连接是否成功
        db = client['admin']
        db.list_collection_names()  # 用于检查连接
        return True

    except Exception as e:
        logger.error(f"Error: {e}")
        return False

if __name__ == "__main__":
    host = "10.0.0.16"  # 替换为你的MongoDB主机名
    port = 27017  # 替换为你的MongoDB端口号，如果不是默认端口
    username = "root"  # 替换为你的MongoDB用户名a
    password = "xtk6AYDSaXh2pEkADD3eTnRR"  # 替换为你的MongoDB密码
    auth_db = "admin"  # 替换为你用于身份验证的MongoDB数据库名称

    while True:
        is_connected = check_mongodb_connection(host, port, username, password, auth_db)
        if is_connected:
            logger.info("Connected to MongoDB")
        else:
            logger.info("Failed to connect to MongoDB")
        
        time.sleep(1)  # 每秒检查一次
