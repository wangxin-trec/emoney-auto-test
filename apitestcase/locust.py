from locust import HttpUser, task, between
import xml.etree.ElementTree as ET
from collections import defaultdict
import re

HEADERS = {
    "Deposit": {"SOAPAction": "deposit"},
    "Withdraw": {"SOAPAction": "withdraw"},
    "GetBalance": {"SOAPAction": "getBalance"},
    "StatusCheck": {"SOAPAction": "statusCheck"}
}

# 定义三个 API 的请求体
BODIES = {
    "Deposit": """<x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://services.soap.valuecardservice.com" xmlns:xsd="http://dto.soap.valuecardservice.com/xsd">
                    <x:Header/>
                    <x:Body>
                        <ser:deposit>
                            <ser:accessKey>kInRLqsxpQkgaZdUU21vGjRpYAaI</ser:accessKey>
                            <ser:dealInfo>
                                <xsd:cardNo>8812960000002014</xsd:cardNo>
                                <xsd:pinCode>000517</xsd:pinCode>
                                <xsd:receiptNo>123456789012345</xsd:receiptNo>
                                <xsd:reqId>123456</xsd:reqId>
                                <xsd:termId>9812909020100</xsd:termId>
                                <xsd:version>020000</xsd:version>
                            </ser:dealInfo>
                            <ser:volume>1</ser:volume>
                            <ser:valueType>A</ser:valueType>
                        </ser:deposit>
                    </x:Body>
                </x:Envelope>""",
    "Withdraw": """<x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://services.soap.valuecardservice.com" xmlns:xsd="http://dto.soap.valuecardservice.com/xsd">
                    <x:Header/>
                    <x:Body>
                        <ser:withdraw>
                            <ser:accessKey>kInRLqsxpQkgaZdUU21vGjRpYAaI</ser:accessKey>
                            <ser:dealInfo>
                                <xsd:cardNo>8812960000002014</xsd:cardNo>
                                <xsd:pinCode>000517</xsd:pinCode>
                                <xsd:receiptNo>123456789012345</xsd:receiptNo>
                                <xsd:reqId>546321</xsd:reqId>
                                <xsd:termId>9812909020100</xsd:termId>
                                <xsd:version>020000</xsd:version>
                            </ser:dealInfo>
                            <ser:volume>1</ser:volume>
                        </ser:withdraw>
                    </x:Body>
                  </x:Envelope>""",
    "GetBalance": """<x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://services.soap.valuecardservice.com" xmlns:xsd="http://dto.soap.valuecardservice.com/xsd">
                      <x:Header/>
                      <x:Body>
                        <ser:getBalance>
                            <ser:accessKey>kInRLqsxpQkgaZdUU21vGjRpYAaI</ser:accessKey>
                            <ser:termId>9812909020100</ser:termId>
                            <xsd:cardNo>8812960000002014</xsd:cardNo>
                            <xsd:pinCode>000517</xsd:pinCode>
                        </ser:getBalance>
                      </x:Body>
                    </x:Envelope>""",
    "StatusCheck": """<x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://services.soap.valuecardservice.com" xmlns:xsd="http://dto.soap.valuecardservice.com/xsd">
                        <x:Header/>
                        <x:Body>
                            <ser:statusCheck>
                                <ser:accessKey>kInRLqsxpQkgaZdUU21vGjRpYAaI</ser:accessKey>
                                <ser:termId>9812909020100</ser:termId>
                                <xsd:cardNo>8812960000002014</xsd:cardNo>
                                <ser:pinCode>000517</ser:pinCode>
                            </ser:statusCheck>
                        </x:Body>
                    </x:Envelope>"""
}

class ApiUser(HttpUser):
    wait_time = between(0, 1)
    host = "https://emoney-test.supay.jp"
    # 用于存储状态码计数的字典
    result_code_count = defaultdict(int)
    @task
    def perform_transactions(self):
        self.validate_response(self.client.post("", data=BODIES["Deposit"], headers=HEADERS["Deposit"], name="/deposit"), "deposit")
        self.validate_response(self.client.post("", data=BODIES["Withdraw"], headers=HEADERS["Withdraw"], name="/withdraw"), "withdraw")
        self.validate_response(self.client.post("", data=BODIES["GetBalance"], headers=HEADERS["GetBalance"], name="/getBalance"), "getBalance")
        self.validate_response(self.client.post("", data=BODIES["StatusCheck"], headers=HEADERS["StatusCheck"], name="/statusCheck"), "statusCheck")

    def validate_response(self, response, action):
        if response.status_code != 200:
            print(f'error {action}: {response.content}')
        result_code_match = re.search(r"<[^:]+:resultCode>(\d+)</[^:]+:resultCode>", str(response.content))
        if result_code_match:
            result_code = result_code_match.group(1)
        else:
            result_code = str(response.content)
        if result_code in self.result_code_count:
            self.result_code_count[result_code] += 1
        else:
            self.result_code_count[result_code] = 1


    def on_stop(self):
        # 测试结束时打印状态码统计
        print("Status code counts:")
        for code, count in self.result_code_count.items():
            print(f"Status Code {code}: {count} times")