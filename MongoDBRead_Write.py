from pymongo import MongoClient, errors
from util.Logger import logger
import time

# MongoDB 连接 URI
uri = "mongodb://root:xtk6AYDSaXh2pEkADD3eTnRR@34.85.41.37:27017/?authSource=admin"

# 连接到 MongoDB
client = MongoClient(uri)

# 选择数据库和集合
db = client["test_database"]
collection = db["test_collection2"]

# 清空集合
collection.delete_many({})

# 测试数据插入
def insert_test_data(num_docs):
    documents = [{"_id": i, "data": "Test data " + str(i)} for i in range(num_docs)]
    try:
        # 批量插入数据
        collection.insert_many(documents)
        logger.info(f"已插入 {num_docs} 条数据")
    except errors.AutoReconnect as e:
        logger.error(f"Connection error: {e}, retrying...")
        time.sleep(5)  # 等待 5 秒后重试
        try:
            # 尝试重新插入
            collection.insert_many(documents)
        except Exception as e:
            logger.error(f"Failed to insert documents after retry: {e}")

# 测试大数据插入
def insert_test_bigdata():
    # 构造一条大数据
    big_data = {'key': 'value' * 1000000}  # 重复"value" 100万次
    big_data2 = {'key': 'value' * 500000}  # 重复"value" 50万次
    # 开始会话
    with client.start_session() as session:
        try:
            # 开始事务
            session.start_transaction()
            # 插入大数据
            collection.insert_one(big_data, session=session)
            time.sleep(5)  # 减少等待时间
            collection.insert_one(big_data2, session=session)
            # 提交事务
            session.commit_transaction()
            logger.info("数据插入成功")
        except Exception as e:
            # 回滚事务
            session.abort_transaction()
            logger.error("在插入过程中发生错误:", e)

# 插入 10 万条数据
# insert_test_data(100000)
insert_test_bigdata()

# 查询当前集合中的文档数量
doc_count = collection.count_documents({})
logger.info(f"当前集合中的文档数量为: {doc_count}")

logger.info("数据插入及查询完成。")
