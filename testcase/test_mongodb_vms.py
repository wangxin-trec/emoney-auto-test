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
    @pytest.mark.run(order=1)
    def test_stop_mongodb_vms(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
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
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    @staticmethod
    def start_single_vm(vm_ops, project_id, vm):
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        if str(operation.status) == ConfigInfo.Status.Done:
            logger.info('start mongodb vm --> done ' + vm["name"])
        return str(operation.status)

    # start all mongodb vm at same time
    @allure.story('Test Start all MongoDB VMs')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=2)
    def test_start_mongodb_vms(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
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
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    #########################################config###############################################
    # stop mongodb-config-1
    @allure.story('Test Stop MongoDB Config 1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=3)
    def test_stop_mongo_config_1(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["config1"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # stop mongodb-config-2
    @allure.story('Test Stop MongoDB Config 2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=4)
    def test_stop_mongo_config_2(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["config2"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # stop mongodb-config-3
    @allure.story('Test Stop MongoDB Config 3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=5)
    def test_stop_mongo_config_3(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["config3"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # start mongodb-config-1
    @allure.story('Test Start MongoDB Config 1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=6)
    def test_stop_mongo_config_1(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["config1"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # start mongodb-config-2
    @allure.story('Test Start MongoDB Config 2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=7)
    def test_stop_mongo_config_2(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["config2"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # start mongodb-config-3
    @allure.story('Test Start MongoDB Config 3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=8)
    def test_stop_mongo_config_3(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["config3"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # restart mongodb-config-1
    @allure.story('Test Restart MongoDB Config 1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=9)
    def test_restart_mongo_config_1(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["config1"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # restart mongodb-config-2
    @allure.story('Test Restart MongoDB Config 2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=10)
    def test_restart_mongo_config_2(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["config2"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # restart mongodb-config-3
    @allure.story('Test Restart MongoDB Config 3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=11)
    def test_restart_mongo_config_3(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["config3"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)
    #########################################config###############################################

    #########################################shard1###############################################
    # stop mongodb-shard1-1
    @allure.story('Test Stop MongoDB shard 1-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=12)
    def test_stop_mongo_shard_1_1(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-1"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # stop mongodb-shard1-2
    @allure.story('Test Stop MongoDB shard 1-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=13)
    def test_stop_mongo_shard_1_2(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-2"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # stop mongodb-shard1-3-arbiter
    @allure.story('Test Stop MongoDB shard 1-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=14)
    def test_stop_mongo_shard_1_3_arbiter(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-3-arbiter"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard1-1
    @allure.story('Test Start MongoDB shard 1-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=15)
    def test_start_mongo_shard_1_1(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-1"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard1-2
    @allure.story('Test Start MongoDB shard 1-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=16)
    def test_start_mongo_shard_1_2(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-2"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard1-3-arbiter
    @allure.story('Test Start MongoDB shard 1-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=17)
    def test_start_mongo_shard_1_3_arbiter(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-3-arbiter"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard1-1
    @allure.story('Test Restart MongoDB shard 1-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=18)
    def test_restart_mongo_shard_1_1(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-1"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard1-2
    @allure.story('Test Restart MongoDB shard 1-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=19)
    def test_restart_mongo_shard_1_2(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-2"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard1-3-arbiter
    @allure.story('Test Restart MongoDB shard 1-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=20)
    def test_restart_mongo_shard_1_3(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard1-3-arbiter"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)
    #########################################shard1###############################################

    #########################################shard2###############################################
    # stop mongodb-shard2-1
    @allure.story('Test Stop MongoDB shard 2-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=21)
    def test_stop_mongo_shard_2_1(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-1"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # stop mongodb-shard2-2
    @allure.story('Test Stop MongoDB shard 2-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=22)
    def test_stop_mongo_shard_2_2(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-2"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # stop mongodb-shard2-3-arbiter
    @allure.story('Test Stop MongoDB shard 2-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=23)
    def test_stop_mongo_shard_2_3_arbiter(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-3-arbiter"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard2-1
    @allure.story('Test Start MongoDB shard 2-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=24)
    def test_start_mongo_shard_2_1(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-1"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard2-2
    @allure.story('Test Start MongoDB shard 1-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=25)
    def test_start_mongo_shard_2_2(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-2"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # start mongodb-shard2-3-arbiter
    @allure.story('Test Start MongoDB shard 2-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=26)
    def test_start_mongo_shard_2_3_arbiter(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-3-arbiter"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard2-1
    @allure.story('Test Restart MongoDB shard 2-1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=27)
    def test_restart_mongo_shard_2_1(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-1"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard2-2
    @allure.story('Test Restart MongoDB shard 2-2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=28)
    def test_restart_mongo_shard_2_2(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-2"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)

    # restart mongodb-shard2-3-arbiter
    @allure.story('Test Restart MongoDB shard 2-3-arbiter')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=29)
    def test_restart_mongo_shard_2_2(self, vm_ops):
        logger.info('test case begin: ' + inspect.currentframe().f_code.co_name)
        vm = MONGODB_VMs["shard2-3-arbiter"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('test case end: ' + inspect.currentframe().f_code.co_name)
    #########################################shard2###############################################