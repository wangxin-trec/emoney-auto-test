from util.Logger import logger
from util.File import FileUtil
from util.Config import ConfigInfo

import pytest,traceback,os

if __name__ == '__main__':
  try:
    version = ConfigInfo.Version
    logger.info('★★★★APIテスト⇒開始★★★★ ' + version)
    testCasePath = ConfigInfo.File.APITestcasePath
    if FileUtil._isExists(testCasePath) and not FileUtil._isFile(testCasePath) and FileUtil._isFolderNotNul(testCasePath) and FileUtil._isExistsFomatFile(testCasePath,'.py'):
        #folderを作成
        FileUtil._createFolder(ConfigInfo.File.APIReportPath)
        FileUtil._createFolder(ConfigInfo.File.APITempJsonPath)
        #臨時Jsonファイルを削除
        FileUtil._rmFile(ConfigInfo.File.APITempJsonPath)
        pytest.main(["-s", testCasePath, "--alluredir", ConfigInfo.File.APITempJsonPath + '/', '--report=brief_report.html','--title=AutoTestReport','--template=2','--cov=' + testCasePath,'--cov-report=html'])
        #テストケースを実行終了、allure報告を作成
        currentReportPath = ConfigInfo.File.APIReportPath + '/main_report'
        os.system(ConfigInfo.ShellCommend.AllureGenerate + ConfigInfo.File.APITempJsonPath + '/' + " -o " + currentReportPath + " --clean")
        #DoubleClickToOpenReport.batファイルを作成
        with open(currentReportPath + '/DoubleClickToOpenReport.bat', 'w') as f:
          f.write(ConfigInfo.ShellCommend.AllureOpen)
          f.close()
        #DoubleClickToOpenReport.shファイルを作成
        with open(currentReportPath + '/OpenReport.sh', 'w') as f:
          f.write("#!/bin/bash\n")
          f.write(ConfigInfo.ShellCommend.AllureOpen)
          f.close()
        os.chmod(currentReportPath + '/OpenReport.sh', 0o755)
    logger.info('★★★★APIテスト⇒終了★★★★ ' + version)
  except Exception as e:
    error_msg = traceback.format_exc()
    logger.error('★★★★APIテスト⇒エラー★★★★：' + error_msg)
