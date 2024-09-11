from util.Logger import logger
from util.File import FileUtil
from util.Config import ConfigInfo

import pytest,traceback,os

if __name__ == '__main__':
  logger.info('''

  /$$$$$$              /$$                     /$$$$$$$$                       /$$    
/$$__  $$            | $$                    |__  $$__/                      | $$     
| $$  \ $$ /$$   /$$ /$$$$$$    /$$$$$$          | $$     /$$$$$$   /$$$$$$$ /$$$$$$   
| $$$$$$$$| $$  | $$|_  $$_/   /$$__  $$         | $$    /$$__  $$ /$$_____/|_  $$_/   
| $$__  $$| $$  | $$  | $$    | $$  \ $$         | $$   | $$$$$$$$|  $$$$$$   | $$     
| $$  | $$| $$  | $$  | $$ /$$| $$  | $$         | $$   | $$_____/ \____  $$  | $$ /$$ 
| $$  | $$|  $$$$$$/  |  $$$$/|  $$$$$$/         | $$   |  $$$$$$$ /$$$$$$$/  |  $$$$/ 
|__/  |__/ \______/    \___/   \______/          |__/    \_______/|_______/    \___/    
                                                                                                                          
''')
  try:
    version = ConfigInfo.Version
    logger.info('★★★★自動化テスト⇒開始★★★★ ' + version)
    testCasePath = ConfigInfo.File.TestCasePath
    if FileUtil._isExists(testCasePath) and not FileUtil._isFile(testCasePath) and FileUtil._isFolderNotNul(testCasePath) and FileUtil._isExistsFomatFile(testCasePath,'.py'):
        #folderを作成
        FileUtil._createFolder(ConfigInfo.File.ReportPath)
        FileUtil._createFolder(ConfigInfo.File.TempJsonPath)
        #臨時Jsonファイルを削除
        FileUtil._rmFile(ConfigInfo.File.TempJsonPath)
        pytest.main(["-s", testCasePath, "--alluredir", ConfigInfo.File.TempJsonPath + '/', '--report=brief_report.html','--title=AutoTestReport','--template=2','--cov=' + testCasePath,'--cov-report=html'])
        #テストケースを実行終了、allure報告を作成
        currentReportPath = ConfigInfo.File.ReportPath + '/main_report'
        os.system(ConfigInfo.ShellCommend.AllureGenerate + ConfigInfo.File.TempJsonPath + '/' + " -o " + currentReportPath + " --clean")
        #DoubleClickToOpenReport.batファイルを作成
        with open(currentReportPath + '/DoubleClickToOpenReport.bat', 'w') as f:
          f.write(ConfigInfo.ShellCommend.AllureOpen)
          f.close()
    logger.info('★★★★自動化テスト⇒終了★★★★ ' + version)
  except Exception as e:
    error_msg = traceback.format_exc()
    logger.error('★★★★自動化テスト⇒エラー★★★★：' + error_msg)
