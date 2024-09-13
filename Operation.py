from google.cloud import compute_v1
from util.Config import ConfigInfo
from util.Logger import logger
import allure, time

class VMOperations:
    def __init__(self, client):
        self.client = client

    @allure.step('Start VM')
    def start_vm(self, project_id, zone, instance_name):
        logger.info('VM Start⇒begin: ' + instance_name)
        operation = self.client.start(project=project_id, zone=zone, instance=instance_name)
        operation = self._wait_for_operation(project_id, zone, operation.name)
        logger.info('VM Start⇒end: ' + instance_name)
        return operation

    @allure.step('Stop VM')
    def stop_vm(self, project_id, zone, instance_name):
        logger.info('VM Stop⇒begin: ' + instance_name)
        operation = self.client.stop(project=project_id, zone=zone, instance=instance_name)
        operation = self._wait_for_operation(project_id, zone, operation.name)
        logger.info('VM Stop⇒end: ' + instance_name)
        return operation

    @allure.step('List VMs')
    def list_vms(self, project_id):
        logger.info('VM List⇒begin')
        request = compute_v1.AggregatedListInstancesRequest(project=project_id)
        vm_list = []
        try:
            response = self.client.aggregated_list(request=request)
            for instance in response:
                if 'instances' in instance:
                    for vm_instance in instance['instances']:
                        vm_list.append({
                            'name': vm_instance.name,
                            'zone': vm_instance.zone
                        })
        except Exception as e:
            logger.error("An error occurred:" + str(e))
        logger.info('VM List⇒end')
        return vm_list

    @allure.step('Wait for operation')
    def _wait_for_operation(self, project_id, zone, operation_name):
        # logger.info('VM Wait⇒begin: ' + operation_name)
        operations_client = compute_v1.ZoneOperationsClient()
        while True:
            operation = operations_client.get(project=project_id, zone=zone, operation=operation_name)
            if str(operation.status) == ConfigInfo.Status.Done:
                if 'error' in operation:
                    raise RuntimeError(f"Operation {operation_name} failed: {operation.error}")
                # logger.info('VM Wait⇒end: ' + operation_name)
                return operation
            # Optionally, sleep for a short period before polling again
            time.sleep(1)

    @allure.step('Get user Input')
    def get_user_input(self):
        try:
            while True:
                user_input = input("Please enter content (Press Enter to skip, type 'exit' to quit): ")
                if user_input == "":
                    print("You pressed Enter without entering any content, continuing to the next step.\n")
                    continue
                if user_input.lower() == 'exit':
                    logger.info("User chose to exit the program.")
                    print("Program has exited.")
                    break
                logger.info(f"User input: {user_input}")
        except KeyboardInterrupt:
            logger.info("Program was manually terminated.")
            print("\nProgram has been manually terminated.")