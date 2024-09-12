from util.Config import ConfigInfo
from util.Logger import logger
from Operation import VMOperations
import allure
import pytest
import concurrent.futures
import inspect

ESDB_VMs = {
    "1": {"name": "eventstoredb-1-test", "zone": "asia-northeast1-a", "ip": "10.0.2.6"},#Follower
    "2": {"name": "eventstoredb-2-test", "zone": "asia-northeast1-b", "ip": "10.0.2.7"},#Follower
    "3": {"name": "eventstoredb-3-test", "zone": "asia-northeast1-c", "ip": "10.0.2.8"} #Leader
}

project_id = "emoney-dev-433104"

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


    ### 启动和宕机操作
    ## 三台都宕机
    # stop all esdb vm at same time >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Stop all ESDB VMs at same time')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=1)
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
    # stop all esdb vm at same time <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    ## 三台都启动
    # start all esdb vm at same time >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Start all ESDB VMs at same time')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=2)
    def test_start_eventstoredb_all(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
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
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # start all esdb vm at same time <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 只让一台启动
    # 只让 node1 启动，node2 和 node3 宕机
    # only start esdb 1 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Start ESDB 1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=3)
    def test_only_start_eventstoredb_1(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        ESDB_VMs_select = {key: ESDB_VMs[key] for key in ["2", "3"]}
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
    # only start esdb 1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 只让一台启动
    # 只让 node2 启动，node1 和 node3 宕机
    # only start esdb 2 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Start ESDB 2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=4)
    def test_only_start_eventstoredb_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = ESDB_VMs["1"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Stop esdb vm --> done ' + vm["name"])
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only start esdb 2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 只让一台启动
    # 只让 node3 启动，node1 和 node2 宕机
    # only start esdb 3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Start ESDB 3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=5)
    def test_only_start_eventstoredb_3(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = ESDB_VMs["2"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Stop esdb vm --> done ' + vm["name"])
        vm = ESDB_VMs["3"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Start esdb vm --> done ' + vm["name"])
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only start esdb 3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 只让两台启动
    # 只让 node1 和 node2 启动，node3宕机
    # only start esdb 1,2 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Start ESDB 1,2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=6)
    def test_only_start_eventstoredb_1_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = ESDB_VMs["3"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Stop esdb vm --> done ' + vm["name"])
        ESDB_VMs_select = {key: ESDB_VMs[key] for key in ["1", "2"]}
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
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only start esdb 1,2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 只让两台启动
    # 只让 node2 和 node3 启动，node1宕机
    # only start esdb 2,3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Start ESDB 2,3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=7)
    def test_only_start_eventstoredb_2_3(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = ESDB_VMs["1"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Stop esdb vm --> done ' + vm["name"])
        vm = ESDB_VMs["3"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Start esdb vm --> done ' + vm["name"])
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only start esdb 2,3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 只让两台启动
    # 只让 node1 和 node3 启动，node2宕机
    # only start esdb 1,3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Start ESDB 1,3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=8)
    def test_only_start_eventstoredb_1_3(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = ESDB_VMs["2"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Stop esdb vm --> done ' + vm["name"])
        vm = ESDB_VMs["1"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Start esdb vm --> done ' + vm["name"])
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only start esdb 1,3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 重启操作
    # 只让一台重启
    # only restart esdb 1 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Restart ESDB 1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=9)
    def test_only_restart_eventstoredb_1(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = ESDB_VMs["2"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(operation.status) == ConfigInfo.Status.Done
        logger.info('Start esdb vm --> done ' + vm["name"])
        vm = ESDB_VMs["1"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('Restart esdb vm --> done ' + vm["name"])
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only restart esdb 1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 重启操作
    # 只让一台重启
    # only restart esdb 2 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Restart ESDB 2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=10)
    def test_only_restart_eventstoredb_2(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = ESDB_VMs["2"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('Restart esdb vm --> done ' + vm["name"])
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only restart esdb 2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 重启操作
    # 只让一台重启
    # only restart esdb 3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Restart ESDB 3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=11)
    def test_only_restart_eventstoredb_3(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        vm = ESDB_VMs["3"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert str(stop_operation.status) == ConfigInfo.Status.Done
        assert str(start_operation.status) == ConfigInfo.Status.Done
        logger.info('Restart esdb vm --> done ' + vm["name"])
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only restart esdb 2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 重启操作
    # 只让两台重启
    # only restart esdb 1,2 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Restart ESDB 1,2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=12)
    def test_only_restart_eventstoredb_1_2(self, vm_ops):
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
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only restart esdb 1,2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 重启操作
    # 只让两台重启
    # only restart esdb 2,3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Restart ESDB 2,3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=13)
    def test_only_restart_eventstoredb_2_3(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        ESDB_VMs_select = {key: ESDB_VMs[key] for key in ["2", "3"]}
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
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only restart esdb 2,3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 重启操作
    # 只让两台重启
    # only restart esdb 1,3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Only Restart ESDB 1,3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=14)
    def test_only_restart_eventstoredb_1_3(self, vm_ops):
        logger.info('test case begin: -------------->' + inspect.currentframe().f_code.co_name)
        ESDB_VMs_select = {key: ESDB_VMs[key] for key in ["1", "3"]}
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
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # only restart esdb 1,3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    ## 三台都重启
    # restart esdb 1,2,3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @allure.story('Test Restart ESDB 1,2,3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=15)
    def test_restart_eventstoredb_all(self, vm_ops):
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
        logger.info('test case end: -------------->' + inspect.currentframe().f_code.co_name)
    # restart esdb 1,2,3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<