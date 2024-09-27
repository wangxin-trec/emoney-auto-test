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
2. run MongoDB_health_check_per_second.py
3. run StartAutoTest.sh in GCP shell
4. run StartMongoDBRead_Write when notice user input automaticlly
Go into the mongos VM
mongosh --host mongo-vm-shard1-1 -u root -p xtk6AYDSaXh2pEkADD3eTnRR
rs.status()
↑可以查询mongo-vm-shard1-1的主备节点状态

mongosh --host mongo-vm-shard2-1 -u root -p xtk6AYDSaXh2pEkADD3eTnRR
rs.status()
↑可以查询mongo-vm-shard2-1的主备节点状态

进入Mongo Compass
sh.status()
↑可以查询集群状态

计算备节点升级为主节点时间（在关闭主节点用例时）
sudo grep "transition to primary" /var/log/mongodb/mongod.log
mongodb的log记录地址: cd /var/log/mongodb/

### 测试API情况
1. 可以直接运行StartAPITest.bat 采用了pytest多线程的方式，结合allure出报告
2. 也可以用locust apitestcase/locust.py 
执行命令：locust -f locustfile.py --headless -u 400 --spawn-rate 400 --autostart --target-rps 400