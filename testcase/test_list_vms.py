from util.Config import ConfigInfo
from util.Logger import logger
import allure,pytest

TEST_CASE_LINK = 'http://www.baidu.com'#Google document link that can be replaced with test case
BUG_LINK = 'http://www.baidu.com'#Google document links that can be replaced with bug records
@allure.epic('Test VM')
@allure.feature('Test List VMs')
@allure.suite('test suite for VM')
class TestListVms:

    @allure.severity('normal')
    @allure.story('Test VM')
    @allure.title('Test to List VMs')
    @allure.description('login the gcp and list the vms')
    @allure.testcase(TEST_CASE_LINK, 'Link to test case')
    @allure.issue(BUG_LINK, 'Links to tested bugs')
    @allure.tag('VM')
    @pytest.mark.flaky(reruns=int(ConfigInfo.TestCaseReRun.Count), reruns_delay=int(ConfigInfo.TestCaseReRun.Delay))
    @pytest.mark.run(order=1)
    def test_list_vms(self, client):
        logger.info('开始')
        instances = client.list(project="emoney-dev-433104", zone="asia-northeast1-a")
        for instance in instances:
            name = instance.name
            logger.info('Instance:' + name)
        assert instances is not None