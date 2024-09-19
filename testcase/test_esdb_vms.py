from util.Config import ConfigInfo
from util.Logger import logger
from Operation import VMOperations
import allure
import pytest
import concurrent.futures
import inspect
import time

ESDB_VMs = {
    "1": {"name": "eventstoredb-1-test", "zone": "asia-northeast1-a", "ip": "10.0.2.6"},#Follower
    "2": {"name": "eventstoredb-2-test", "zone": "asia-northeast1-b", "ip": "10.0.2.7"},#Follower
    "3": {"name": "eventstoredb-3-test", "zone": "asia-northeast1-c", "ip": "10.0.2.8"} #Leader
}

project_id = "emoney-dev-433104"

@pytest.fixture(scope='function', autouse=True)
def add_delay_after_test():
    yield
    logger.info('Delay 30s =================>')
    time.sleep(30) # 每条用例执行完都延时30s
    logger.info('Delay 30s <=================')

@allure.epic('Test ESDB VMs')
class TestAllESDBVM:

    @pytest.fixture(scope='class')
    def vm_ops(self, client):
        return VMOperations(client)

    @staticmethod
    def stop_single_vm(vm_ops, project_id, vm):
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        if str(operation.status) == ConfigInfo.Status.Done:
            logger.info('stop esdb vm --> done ' + vm["name"])
        return str(operation.status)

    @staticmethod
    def start_single_vm(vm_ops, project_id, vm):
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        if str(operation.status) == ConfigInfo.Status.Done:
            logger.info('start esdb vm --> done ' + vm["name"])
        return str(operation.status)

    ### 一台备机停机
    @allure.story('Test Stop 1 follower: node1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=1)
    def test_stop_follower_node_1(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = ESDB_VMs["1"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Stop esdb vm --> done ' + vm["name"])
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input() ## 暂停，等待用户输入确认，给vm, Node 一定时间
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Start esdb vm --> done ' + vm["name"]) ## 不影响下一个测试用例
        vm_ops.get_user_input() ## 暂停，等待用户输入确认，给vm, Node 一定时间

    ### 两台备机停机
    @allure.story('Test Stop 2 follower: node1, node2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=2)
    def test_stop_follower_node_1_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        ESDB_VMs_select = {key: ESDB_VMs[key] for key in ["1", "2"]}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.stop_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in ESDB_VMs_select.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to stop VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input() ## 暂停，等待用户输入确认，给vm, Node 一定时间
        # 开启VM 1,2
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.start_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in ESDB_VMs_select.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to start VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input() ## 暂停，等待用户输入确认，给vm, Node 一定时间

    ### 主机停机
    @allure.story('Test Stop 1 Leader: node3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=3)
    def test_stop_leader_node_3(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = ESDB_VMs["3"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Stop esdb vm --> done ' + vm["name"])
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input() ## 暂停，等待用户输入确认，给vm, Node 一定时间
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Start esdb vm --> done ' + vm["name"]) ## 不影响下一个测试用例
        vm_ops.get_user_input() ## 暂停，等待用户输入确认，给vm, Node 一定时间

    ### 集群停机（三台VM都宕机）
    @allure.story('Test Stop all ESDB VMs at same time')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=4)
    def test_stop_eventstoredb_all(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.stop_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in ESDB_VMs.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to stop VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input() ## 暂停，等待用户输入确认，给vm, Node 一定时间
        # 开启三台VM
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.start_single_vm, vm_ops, project_id, vm): vm_key 
                for vm_key, vm in ESDB_VMs.items()
            }
            for future in concurrent.futures.as_completed(futures):
                vm_key = futures[future]
                try:
                    status = future.result()
                    assert str(status) == ConfigInfo.Status.Done, f"Failed to start VM: {vm_key}"
                except Exception as exc:
                    logger.error(f'VM {vm_key} generated an exception: {exc}')
        vm_ops.get_user_input() ## 暂停，等待用户输入确认，给vm, Node 一定时间