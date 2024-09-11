from util.Config import ConfigInfo
from util.Logger import logger
from Operation import VMOperations
import allure
import pytest

ESDB_VMs = {
    "1": {"name": "eventstoredb-1-test", "zone": "asia-northeast1-a"},
    "2": {"name": "eventstoredb-2-test", "zone": "asia-northeast1-b"},
    "3": {"name": "eventstoredb-3-test", "zone": "asia-northeast1-c"}
}

project_id = "emoney-dev-433104"

@allure.epic('Test ESDB VMs')
class TestAllESDBVM:

    @pytest.fixture(scope='class')
    def vm_ops(self, client):
        return VMOperations(client)

    # stop all esdb vm
    @allure.story('Test Stop all ESDB VMs')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=1)
    def test_stop_esdb_vms(self, vm_ops):
        for vm_key in ESDB_VMs:
            vm = ESDB_VMs[vm_key]
            operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
            assert operation.status == 'DONE'
            logger.info('stop esdb vm --> done ' + vm["name"])

    # start all esdb vm
    @allure.story('Test Start all ESDB VMs')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=2)
    def test_start_esdb_vms(self, vm_ops):
        for vm_key in ESDB_VMs:
            vm = ESDB_VMs[vm_key]
            operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
            assert operation.status == 'DONE'
            logger.info('start esdb vm --> done ' + vm["name"])

    # stop esdb 1
    @allure.story('Test Stop ESDB 1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=3)
    def test_stop_eventstoredb_1(self, vm_ops):
        vm = ESDB_VMs["1"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert operation.status == 'DONE'
        logger.info('Stop esdb vm --> done ' + vm["name"])

    # stop esdb 2
    @allure.story('Test Stop ESDB 2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=4)
    def test_stop_eventstoredb_2(self, vm_ops):
        vm = ESDB_VMs["2"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert operation.status == 'DONE'
        logger.info('Stop esdb vm --> done ' + vm["name"])

    # stop esdb 3
    @allure.story('Test Stop ESDB 3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=5)
    def test_stop_eventstoredb_3(self, vm_ops):
        vm = ESDB_VMs["3"]
        operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        assert operation.status == 'DONE'
        logger.info('Stop esdb vm --> done ' + vm["name"])

    # start esdb 1
    @allure.story('Test Start ESDB 1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=6)
    def test_start_eventstoredb_1(self, vm_ops):
        vm = ESDB_VMs["1"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert operation.status == 'DONE'
        logger.info('Start esdb vm --> done ' + vm["name"])

    # start esdb 2
    @allure.story('Test Start ESDB 2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=7)
    def test_start_eventstoredb_2(self, vm_ops):
        vm = ESDB_VMs["2"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert operation.status == 'DONE'
        logger.info('Start esdb vm --> done ' + vm["name"])

    # start esdb 3
    @allure.story('Test Start ESDB 3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=8)
    def test_start_eventstoredb_3(self, vm_ops):
        vm = ESDB_VMs["3"]
        operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert operation.status == 'DONE'
        logger.info('Start esdb vm --> done ' + vm["name"])

    # restart esdb 1
    @allure.story('Test Restart ESDB 1')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=9)
    def test_restart_eventstoredb_1(self, vm_ops):
        vm = ESDB_VMs["1"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert stop_operation.status == 'DONE'
        assert start_operation.status == 'DONE'
        logger.info('Restart esdb vm --> done ' + vm["name"])

    # restart esdb 2
    @allure.story('Test Restart ESDB 2')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=10)
    def test_restart_eventstoredb_2(self, vm_ops):
        vm = ESDB_VMs["2"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert stop_operation.status == 'DONE'
        assert start_operation.status == 'DONE'
        logger.info('Restart esdb vm --> done ' + vm["name"])

    # restart esdb 3
    @allure.story('Test Restart ESDB 3')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=11)
    def test_restart_eventstoredb_3(self, vm_ops):
        vm = ESDB_VMs["3"]
        stop_operation = vm_ops.stop_vm(project_id, vm["zone"], vm["name"])
        start_operation = vm_ops.start_vm(project_id, vm["zone"], vm["name"])
        assert stop_operation.status == 'DONE'
        assert start_operation.status == 'DONE'
        logger.info('Restart esdb vm --> done ' + vm["name"])