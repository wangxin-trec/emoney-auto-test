from util.Logger import logger
from util.Common import Common
from util.Config import ConfigInfo
from google.cloud import compute_v1
import pytest,os

@pytest.fixture
def client():
    currentTestCaseName = Common._validatePath(os.environ.get('PYTEST_CURRENT_TEST').split(' ')[0])
    logger.info('>>>>TestCase is ' + currentTestCaseName + '>>>> begin')
    os.system('gcloud auth login')
    client = compute_v1.InstancesClient()
    yield client
    logger.info('<<<<TestCase is ' + currentTestCaseName + '<<<< end')
