# emoney-auto-test
Preparation: Make sure Java and Allure tools are installed and environment variables are properly set.

1. Push the project to the GCP user directory.
2. Execute cd emoney-auto-test.
3. Make StartAutoTest.sh executable.
4. Confirm the test case scripts to be executed, located in the testcase folder.
5. Execute StartAutoTest.sh, and after completion, check the Allure report in the main_report directory.

# if you want to record esdb gossip info, should exec StartAutoGetGossipData.py(click StartAutoGetGossipDat.bat if your os is windows.), should input 'Ctrl + C' if you want to exit.(also: should use wireGuard vpn)

### test esdb monkey test
1. delete test_mongodb_vms.py in testcase folder
2. run StartAutoGetGossipData.bat locally
3. run StartAutoTest.sh in GCP shell
4. run StartESDBRead_Write.bat when notice user input automaticlly
※`sudo systemctl status eventstore` should be executed if you started VM but cannot get gossip from esdb, if eventstore service is not running, then execute `sudo systemctl start eventstore`


### test mongodb monkey test
1. delete teste_esdb_vms.py in testcase folder
...