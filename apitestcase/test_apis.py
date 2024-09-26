from util.Config import ConfigInfo
import pytest
import requests
import allure
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import re

# Define API endpoint and headers
# 定义三个 API 的 URL 和请求头信息
API_HOST = "https://emoney-test.supay.jp/"
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

# Define the number of requests for the stress test
CONCURRENCY_LEVEL = 400  # Number of concurrent threads
TOTAL_REQUESTS = 400    # Total number of requests

# 全局变量用于存储统计数据
total_requests = 0
success_count = 0
failure_count = 0
total_time = 0
total_data_received = 0
response_times = []
result_code_count = {}

# 定义 class 级别的 fixture
@allure.step("Collecting final statistics")
@pytest.fixture(scope="session", autouse=True)
def gather_statistics():
    global total_requests, success_count, failure_count, total_time, total_data_received, response_times, result_code_count
    start_time = time.time() 
    yield
    end_time = time.time()
    total_time = end_time - start_time
    error_rate = (failure_count / total_requests) * 100 if total_requests else 0
    total_data_received_mb = total_data_received / (1024 * 1024)
    requests_per_second = total_requests / total_time if total_time > 0 else 0
    success_requests_per_second = success_count / total_time if total_time > 0 else 0
    max_response_time = max(response_times) if response_times else 0
    min_response_time = min(response_times) if response_times else 0
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0

    # 将统计信息附加到 Allure 报告中
    with allure.step("Collecting final statistics"):
        allure.attach(f"{total_requests}", name="Total Requests", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"{total_time:.2f} seconds", name="Total Time", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"{success_count}", name="Successful Requests", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"{failure_count}", name="Failed Requests", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"{error_rate:.2f}%", name="Error Rate", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"{total_data_received_mb:.2f} MB", name="Total Data Received (MB)", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"{requests_per_second:.2f} requests/sec", name="Requests Per Second", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"{success_requests_per_second:.2f} requests/sec", name="Successful Requests Per Second", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"{max_response_time:.2f} seconds", name="Max Response Time", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"{min_response_time:.2f} seconds", name="Min Response Time", attachment_type=allure.attachment_type.TEXT)
        allure.attach(f"{avg_response_time:.2f} seconds", name="Average Response Time", attachment_type=allure.attachment_type.TEXT)
        # Attach resultCode statistics
        for code, count in result_code_count.items():
            allure.attach(f"{count}", name=f"ResultCode {code}", attachment_type=allure.attachment_type.TEXT)

class TestApi:

    @staticmethod
    def send_request(api_name):
        """Send a single SOAP request to the API."""
        global total_requests, success_count, failure_count, total_data_received, response_times, result_code_count
        try:
            start_time = time.time()  # Record start time of the request
            response = requests.post(API_HOST, headers=HEADERS[api_name], data=BODIES[api_name])
            end_time = time.time()  # Record end time of the request

            # Calculate response time and append to list
            response_time = end_time - start_time
            allure.attach(f"{response_time:.2f} seconds", name="Response Time", attachment_type=allure.attachment_type.TEXT)
            total_requests += 1 
            # Check status code
            if response.status_code == 200:
                total_data_received += len(response.content)  # Calculate total data received
                # Extract resultCode from the response
                result_code_match = re.search(r"<\w+:resultCode>(\d+)</\w+:resultCode>", response.text)
                if result_code_match:
                    result_code = result_code_match.group(1)
                    if result_code == '200':
                        success_count += 1
                    else:
                        failure_count += 1
                    if result_code in result_code_count:
                        result_code_count[result_code] += 1
                    else:
                        result_code_count[result_code] = 1
            else:
                failure_count += 1

            allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.XML)
        except Exception as e:
            failure_count += 1
            allure.attach(str(e), name="Request Error", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Stress test for API endpoint")
    @pytest.mark.parametrize("api_name", ["Deposit", "Withdraw", "GetBalance", "StatusCheck"])
    def test_stress_api(self, api_name):
        """API stress test using pytest and allure with concurrent requests."""
        with ThreadPoolExecutor(max_workers=CONCURRENCY_LEVEL) as executor:
            futures = [executor.submit(self.send_request, api_name) for _ in range(TOTAL_REQUESTS)]
            for future in as_completed(futures):
                future.result()
