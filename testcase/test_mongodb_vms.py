from util.Config import ConfigInfo
from util.Logger import logger
from Operation import VMOperations
import allure,pytest
import concurrent.futures
import inspect
import time

MONGODB_VMs = {
    "mongo-vm-shard1-1": {"name": "mongo-vm-shard1-1", "zone": "asia-northeast1-b"},
    "mongo-vm-shard1-2": {"name": "mongo-vm-shard1-2", "zone": "asia-northeast1-b"},
    "mongo-vm-shard1-3-arbiter": {"name": "mongo-vm-shard1-3-arbiter", "zone": "asia-northeast1-b"},
    "mongo-vm-shard2-1": {"name": "mongo-vm-shard2-1", "zone": "asia-northeast1-c"},
    "mongo-vm-shard2-2": {"name": "mongo-vm-shard2-2", "zone": "asia-northeast1-c"},
    "mongo-vm-shard2-3-arbiter": {"name": "mongo-vm-shard2-3-arbiter", "zone": "asia-northeast1-c"}
}

project_id = "emoney-dev-433104"

@pytest.fixture(scope='function', autouse=True)
def add_delay_after_test():
    yield
    logger.info('Delay 10s =================>')
    time.sleep(30) # 每条用例执行完都延时10s
    logger.info('Delay 10s <=================')

@allure.epic('Test MongoDB VMs')
class TestAllMongoDBVM:

    @staticmethod
    def stop_single_vm(vm_ops, project_id, vm):
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        if str(operation.status) == ConfigInfo.Status.Done:
            logger.info('stop mongo vm --> done ' + vm["name"])
        return str(operation.status)

    @staticmethod
    def start_single_vm(vm_ops, project_id, vm):
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        if str(operation.status) == ConfigInfo.Status.Done:
            logger.info('start mongo vm --> done ' + vm["name"])
        return str(operation.status)


    @pytest.fixture(scope='class')
    def vm_ops(self, client):
        return VMOperations(client)

    @allure.story('停止一台备机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=1)
    def test_stop_1_secondary(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点：")
        node = vm_ops.get_user_input("请输入想停止的次节点：") # mongo-vm-shard1-1，mongo-vm-shard1-2，mongo-vm-shard2-1， mongo-vm-shard2-2
        vm = MONGODB_VMs[node]
        logger.info(str(vm))
        operation1 = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation1.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：") ## 暂停, 输入测试结果：当前mongodb是否可读可写
        operation2 = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation2.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('停止一台Arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=2)
    def test_stop_1_arbiter(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点，arbiter节点将自动停止：")
        vm = MONGODB_VMs["mongo-vm-shard1-3-arbiter"]
        operation1 = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation1.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：") ## 暂停, 输入测试结果：当前mongodb是否可读可写
        operation2 = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation2.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('停止备机和Arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=3)
    def test_stop_1_secondary_1_arbiter(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点：")
        node1 = vm_ops.get_user_input("请输入想停止的次节点，arbiter节点将自动停止：")
        vm_secondary = MONGODB_VMs[node1]
        vm_arbiter = MONGODB_VMs["mongo-vm-shard1-3-arbiter"]
        operation1 = vm_ops.stop_vm(project_id, vm_secondary["zone"], vm_secondary["name"])
        operation2 = vm_ops.stop_vm(project_id, vm_arbiter["zone"], vm_arbiter["name"])
        assert str(operation1.status) == ConfigInfo.Status.Done
        assert str(operation2.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：") ## 暂停, 输入测试结果：当前mongodb是否可读可写
        operation3 = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        operation4 = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation3.status) == ConfigInfo.Status.Done
        assert str(operation4.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('主机停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=4)
    def test_stop_1_primary(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点：")
        node = vm_ops.get_user_input("请输入想停止的主节点：")
        vm = MONGODB_VMs[node]
        operation1 = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation1.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：") ## 暂停, 输入测试结果：当前mongodb是否可读可写
        operation2 = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation2.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('主机和备机停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=5)
    def test_stop_1_primary_1_secondary(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点：")
        node1 = vm_ops.get_user_input("请输入想停止的主节点：")
        vm1 = MONGODB_VMs[node1]
        operation1 = vm_ops.stop_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation1.status) == ConfigInfo.Status.Done
        node2 = vm_ops.get_user_input("请输入想停止的次节点：")
        vm2 = MONGODB_VMs[node2]
        operation2 = vm_ops.stop_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation2.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：") ## 暂停, 输入测试结果：当前mongodb是否可读可写
        operation3 = vm_ops.start_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation3.status) == ConfigInfo.Status.Done
        operation4 = vm_ops.start_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation4.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('主机和Arbiter停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=6)
    def test_stop_1_primary_1_arbiter(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点：")
        node1 = vm_ops.get_user_input("请输入想停止的主节点, arbiter节点将自动停止：")
        vm1 = MONGODB_VMs[node1]
        operation1 = vm_ops.stop_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation1.status) == ConfigInfo.Status.done
        vm2 = MONGODB_VMs["mongo-vm-shard1-3-arbiter"]
        operation2 = vm_ops.stop_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation2.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：") ## 暂停, 输入测试结果：当前mongodb是否可读可写
        operation3 = vm_ops.start_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation3.status) == ConfigInfo.Status.Done
        operation4 = vm_ops.start_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation4.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('shard1停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=7)
    def test_stop_1_shard(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点，所有节点将自动停止：")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.stop_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in MONGODB_VMs.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to stop VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.start_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in MONGODB_VMs.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to start VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('所有备机停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=8)
    def test_stop_all_secondary(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点：")
        node1 = vm_ops.get_user_input("请输入想停止的第一个备用节点：")
        vm1 = MONGODB_VMs[node1]
        operation1 = vm_ops.stop_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation1.status) == ConfigInfo.Status.Done
        node2 = vm_ops.get_user_input("请输入想停止的第二个备用节点：")
        vm2 = MONGODB_VMs[node2]
        operation2 = vm_ops.stop_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation2.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：")
        operation3 = vm_ops.start_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation3.status) == ConfigInfo.Status.Done
        operation4 = vm_ops.start_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation4.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('所有arbiter停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=9)
    def test_stop_all_arbiter(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点, arbiter节点将自动停止：")
        MONGODB_VMs_select = {key: ESDB_VMs[key] for key in ["mongo-vm-shard1-3-arbiter", "mongo-vm-shard2-3-arbiter"]}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.stop_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in MONGODB_VMs_select.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to stop VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.start_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in MONGODB_VMs_select.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to start VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('所有备机和arbiter停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=10)
    def test_stop_all_secondary_arbiter(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点, arbiter节点将自动停止：")
        node1 = vm_ops.get_user_input("请输入想停止的第一个备用节点：")
        vm1 = MONGODB_VMs[node1]
        operation1 = vm_ops.stop_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation1.status) == ConfigInfo.Status.Done
        node2 = vm_ops.get_user_input("请输入想停止的第二个备用节点，arbiter节点将自动停止：")
        vm2 = MONGODB_VMs[node2]
        operation2 = vm_ops.stop_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation2.status) == ConfigInfo.Status.Done
        MONGODB_VMs_select = {key: ESDB_VMs[key] for key in ["mongo-vm-shard1-3-arbiter", "mongo-vm-shard2-3-arbiter"]}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.stop_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in MONGODB_VMs_select.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to stop VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.start_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in MONGODB_VMs_select.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to start VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('所有主机停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=11)
    def test_stop_all_primary(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点：")
        node1 = vm_ops.get_user_input("请输入想停止的第一个主节点：")
        vm1 = MONGODB_VMs[node1]
        operation1 = vm_ops.stop_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation1.status) == ConfigInfo.Status.Done
        node2 = vm_ops.get_user_input("请输入想停止的第二个主节点：")
        vm2 = MONGODB_VMs[node2]
        operation2 = vm_ops.stop_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation2.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：")
        operation3 = vm_ops.start_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation3.status) == ConfigInfo.Status.Done
        operation4 = vm_ops.start_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation4.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('所有主机和备机停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=12)
    def test_stop_all_primary_secondary(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点：")
        node1 = vm_ops.get_user_input("请输入想停止的第一个主节点：")
        vm1 = MONGODB_VMs[node1]
        operation1 = vm_ops.stop_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation1.status) == ConfigInfo.Status.Done
        node2 = vm_ops.get_user_input("请输入想停止的第二个主节点：")
        vm2 = MONGODB_VMs[node2]
        operation2 = vm_ops.stop_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation2.status) == ConfigInfo.Status.Done
        node3 = vm_ops.get_user_input("请输入想停止的第一个备节点：")
        vm3 = MONGODB_VMs[node3]
        operation3 = vm_ops.stop_vm(project_id, vm3["zone"], vm3["name"])
        assert str(operation3.status) == ConfigInfo.Status.Done
        node4 = vm_ops.get_user_input("请输入想停止的第二个备节点：")
        vm4 = MONGODB_VMs[node4]
        operation4 = vm_ops.stop_vm(project_id, vm4["zone"], vm4["name"])
        assert str(operation4.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：")
        operation5 = vm_ops.start_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation5.status) == ConfigInfo.Status.Done
        operation6 = vm_ops.start_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation6.status) == ConfigInfo.Status.Done
        operation7 = vm_ops.start_vm(project_id, vm3["zone"], vm3["name"])
        assert str(operation7.status) == ConfigInfo.Status.Done
        operation8 = vm_ops.start_vm(project_id, vm4["zone"], vm4["name"])
        assert str(operation8.status) == ConfigInfo.Status.Done
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('所有主机和arbiter停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=13)
    def test_stop_all_primary_arbiter(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点：")
        node1 = vm_ops.get_user_input("请输入想停止的第一个主节点：")
        vm1 = MONGODB_VMs[node1]
        operation1 = vm_ops.stop_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation1.status) == ConfigInfo.Status.Done
        node2 = vm_ops.get_user_input("请输入想停止的第二个主节点, 所有的arbiter将自动停机：")
        vm2 = MONGODB_VMs[node2]
        operation2 = vm_ops.stop_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation2.status) == ConfigInfo.Status.Done
        MONGODB_VMs_select = {key: ESDB_VMs[key] for key in ["mongo-vm-shard1-3-arbiter", "mongo-vm-shard2-3-arbiter"]}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.stop_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in MONGODB_VMs_select.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to stop VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：")
        operation5 = vm_ops.stop_vm(project_id, vm1["zone"], vm1["name"])
        assert str(operation5.status) == ConfigInfo.Status.Done
        operation6 = vm_ops.stop_vm(project_id, vm2["zone"], vm2["name"])
        assert str(operation6.status) == ConfigInfo.Status.Done
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.start_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in MONGODB_VMs_select.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to start VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @allure.story('所有主机和arbiter停机')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=14)
    def test_stop_all_shard(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input("请输入查询结果：谁是主节点，谁是备用节点：")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.stop_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in MONGODB_VMs.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to stop VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input("输入当前mongodb是否可读可写，节点将自动恢复：")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.start_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in MONGODB_VMs.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to start VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input("等待节点恢复正常")
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)