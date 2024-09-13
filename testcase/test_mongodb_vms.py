from util.Config import ConfigInfo
from util.Logger import logger
from Operation import VMOperations
import allure,pytest
import concurrent.futures
import inspect

MONGODB_VMs = {
    "config1": {"name": "mongo-vm-config1", "zone": "asia-northeast1-a"},
    "config2": {"name": "mongo-vm-config2", "zone": "asia-northeast1-a"},
    "config3": {"name": "mongo-vm-config3", "zone": "asia-northeast1-a"},
    "shard1-1": {"name": "mongo-vm-shard1-1", "zone": "asia-northeast1-b"},
    "shard1-2": {"name": "mongo-vm-shard1-2", "zone": "asia-northeast1-b"},
    "shard1-3-arbiter": {"name": "mongo-vm-shard1-3-arbiter", "zone": "asia-northeast1-b"},
    "shard2-1": {"name": "mongo-vm-shard2-1", "zone": "asia-northeast1-c"},
    "shard2-2": {"name": "mongo-vm-shard2-2", "zone": "asia-northeast1-c"},
    "shard2-3-arbiter": {"name": "mongo-vm-shard2-3-arbiter", "zone": "asia-northeast1-c"}
}

project_id = "emoney-dev-433104"

@pytest.fixture(scope='function', autouse=True)
def add_delay_after_test():
    yield
    logger.info('Delay 120s =================>')
    time.sleep(120) # 每条用例执行完都延时2min
    logger.info('Delay 120s <=================')

@allure.epic('Test MongoDB VMs')
class TestAllMongoDBVM:

    @pytest.fixture(scope='class')
    def vm_ops(self, client):
        return VMOperations(client)

    @staticmethod
    def stop_single_vm(vm_ops, project_id, vm):
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        if str(operation.status) == ConfigInfo.Status.Done:
            logger.info('stop mongodb vm --> done ' + vm["name"])
        return str(operation.status)

    # stop all mongodb vm at same time
    @allure.story('Test Stop all MongoDB VMs')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=30)
    def test_stop_mongodb_vms(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
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
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=31)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    @staticmethod
    def start_single_vm(vm_ops, project_id, vm):
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        if str(operation.status) == ConfigInfo.Status.Done:
            logger.info('start mongodb vm --> done ' + vm["name"])
        return str(operation.status)

    # start all mongodb vm at same time
    @allure.story('Test Start all MongoDB VMs')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=32)
    def test_start_mongodb_vms(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
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
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=33)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    #########################################config###############################################
    # stop mongodb-config-1
    # @allure.story('Test Stop MongoDB Config 1')
    # @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    # @pytest.mark.run(order=22)
    # def test_stop_mongo_config_1(self, vm_ops):
    #     logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
    #     vm = MONGODB_VMs["config1"]
    #     operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
    #     assert str(operation.status) == ConfigInfo.Status.Done
    #     logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # # stop mongodb-config-2
    # @allure.story('Test Stop MongoDB Config 2')
    # @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    # @pytest.mark.run(order=23)
    # def test_stop_mongo_config_2(self, vm_ops):
    #     logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
    #     vm = MONGODB_VMs["config2"]
    #     operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
    #     assert str(operation.status) == ConfigInfo.Status.Done
    #     logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # # stop mongodb-config-3
    # @allure.story('Test Stop MongoDB Config 3')
    # @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    # @pytest.mark.run(order=24)
    # def test_stop_mongo_config_3(self, vm_ops):
    #     logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
    #     vm = MONGODB_VMs["config3"]
    #     operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
    #     assert str(operation.status) == ConfigInfo.Status.Done
    #     logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # # start mongodb-config-1
    # @allure.story('Test Start MongoDB Config 1')
    # @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    # @pytest.mark.run(order=25)
    # def test_stop_mongo_config_1(self, vm_ops):
    #     logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
    #     vm = MONGODB_VMs["config1"]
    #     operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
    #     assert str(operation.status) == ConfigInfo.Status.Done
    #     logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # # start mongodb-config-2
    # @allure.story('Test Start MongoDB Config 2')
    # @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    # @pytest.mark.run(order=26)
    # def test_stop_mongo_config_2(self, vm_ops):
    #     logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
    #     vm = MONGODB_VMs["config2"]
    #     operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
    #     assert str(operation.status) == ConfigInfo.Status.Done
    #     logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # # start mongodb-config-3
    # @allure.story('Test Start MongoDB Config 3')
    # @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    # @pytest.mark.run(order=27)
    # def test_stop_mongo_config_3(self, vm_ops):
    #     logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
    #     vm = MONGODB_VMs["config3"]
    #     operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
    #     assert str(operation.status) == ConfigInfo.Status.Done
    #     logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # # restart mongodb-config-1
    # @allure.story('Test Restart MongoDB Config 1')
    # @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    # @pytest.mark.run(order=28)
    # def test_restart_mongo_config_1(self, vm_ops):
    #     logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
    #     vm = MONGODB_VMs["config1"]
    #     stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
    #     start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
    #     assert str(stop_operation.status) == ConfigInfo.Status.Done
    #     assert str(start_operation.status) == ConfigInfo.Status.Done
    #     logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # # restart mongodb-config-2
    # @allure.story('Test Restart MongoDB Config 2')
    # @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    # @pytest.mark.run(order=29)
    # def test_restart_mongo_config_2(self, vm_ops):
    #     logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
    #     vm = MONGODB_VMs["config2"]
    #     stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
    #     start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
    #     assert str(stop_operation.status) == ConfigInfo.Status.Done
    #     assert str(start_operation.status) == ConfigInfo.Status.Done
    #     logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # # restart mongodb-config-3
    # @allure.story('Test Restart MongoDB Config 3')
    # @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    # @pytest.mark.run(order=30)
    # def test_restart_mongo_config_3(self, vm_ops):
    #     logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
    #     vm = MONGODB_VMs["config3"]
    #     stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
    #     start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
    #     assert str(stop_operation.status) == ConfigInfo.Status.Done
    #     assert str(start_operation.status) == ConfigInfo.Status.Done
    #     logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    #########################################config###############################################

    #########################################shard1###############################################
    # stop mongodb-shard1-1
    @allure.story('Test Stop MongoDB shard 1-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=34)
    def test_stop_mongo_shard_1_1(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-1"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=35)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # stop mongodb-shard1-2
    @allure.story('Test Stop MongoDB shard 1-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=36)
    def test_stop_mongo_shard_1_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-2"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=37)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # stop mongodb-shard1-3-arbiter
    @allure.story('Test Stop MongoDB shard 1-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=38)
    def test_stop_mongo_shard_1_3_arbiter(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-3-arbiter"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=39)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard1-1
    @allure.story('Test Start MongoDB shard 1-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=40)
    def test_start_mongo_shard_1_1(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-1"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=41)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard1-2
    @allure.story('Test Start MongoDB shard 1-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=42)
    def test_start_mongo_shard_1_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-2"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=43)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard1-3-arbiter
    @allure.story('Test Start MongoDB shard 1-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=44)
    def test_start_mongo_shard_1_3_arbiter(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-3-arbiter"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=45)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard1-1
    @allure.story('Test Restart MongoDB shard 1-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=46)
    def test_restart_mongo_shard_1_1(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-1"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=47)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard1-2
    @allure.story('Test Restart MongoDB shard 1-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=48)
    def test_restart_mongo_shard_1_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-2"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=49)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard1-3-arbiter
    @allure.story('Test Restart MongoDB shard 1-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=50)
    def test_restart_mongo_shard_1_3(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-3-arbiter"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=51)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    #########################################shard1###############################################

    #########################################shard2###############################################
    # stop mongodb-shard2-1
    @allure.story('Test Stop MongoDB shard 2-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=52)
    def test_stop_mongo_shard_2_1(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-1"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=53)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # stop mongodb-shard2-2
    @allure.story('Test Stop MongoDB shard 2-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=54)
    def test_stop_mongo_shard_2_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-2"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=55)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # stop mongodb-shard2-3-arbiter
    @allure.story('Test Stop MongoDB shard 2-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=56)
    def test_stop_mongo_shard_2_3_arbiter(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-3-arbiter"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=57)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard2-1
    @allure.story('Test Start MongoDB shard 2-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=58)
    def test_start_mongo_shard_2_1(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-1"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=59)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard2-2
    @allure.story('Test Start MongoDB shard 1-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=60)
    def test_start_mongo_shard_2_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-2"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=61)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard2-3-arbiter
    @allure.story('Test Start MongoDB shard 2-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=62)
    def test_start_mongo_shard_2_3_arbiter(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-3-arbiter"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=63)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard2-1
    @allure.story('Test Restart MongoDB shard 2-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=64)
    def test_restart_mongo_shard_2_1(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-1"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=65)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard2-2
    @allure.story('Test Restart MongoDB shard 2-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=66)
    def test_restart_mongo_shard_2_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-2"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=67)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard2-3-arbiter
    @allure.story('Test Restart MongoDB shard 2-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=68)
    def test_restart_mongo_shard_2_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-3-arbiter"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)

    # query all node info by user
    @allure.story('query all node info by user')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=69)
    def test_input_all_node_info(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm_ops.get_user_input()
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    #########################################shard2###############################################