from util.Logger import logger
import requests
import threading
import time


esdb_nodes = [
    'http://10.0.2.6:2113/gossip?format=json',
    'http://10.0.2.7:2113/gossip?format=json',
    'http://10.0.2.8:2113/gossip?format=json'
]

def fetch_gossip_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return None

def worker(url):
    while True:
        data = fetch_gossip_data(url)
        if data is not None:
            logger.info(f"Gossip data from {url}: {data}")
        time.sleep(1)

def main():
    threads = []
    for url in esdb_nodes:
        t = threading.Thread(target=worker, args=(url,))
        t.start()
        threads.append(t)
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        logger.info("Program interrupted and stopped.")
        print("Program interrupted and stopped.")

if __name__ == '__main__':
    main()