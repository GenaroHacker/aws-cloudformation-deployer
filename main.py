import boto3
import json
import botocore.exceptions


class Stack:
    def __init__(self, cf_client, stack_name):
        """
        Initializes the CloudFormation manager class with a CloudFormation client and the stack name.

        :param cf_client: The CloudFormation client.
        :param stack_name: Name of the stack managed by this instance.
        """
        self.cf_client = cf_client
        self.stack_name = stack_name

    def create(self, template_body_json):
        """
        Creates the CloudFormation stack if it does not already exist. If the stack already exists,
        handle according to the application's needs (e.g., update, ignore, raise an exception).

        :param template_body_json: JSON-formatted string of the template body.
        """
        # First, check if the stack already exists
        status, _ = self.describe()
        if status is not None:
            # Stack exists, handle accordingly. This example simply returns a message,
            # but you could also update the stack or take other actions.
            return {"message": f"Stack {self.stack_name} already exists. No action taken."}

        # If the stack does not exist, proceed to create it
        try:
            response = self.cf_client.create_stack(
                StackName=self.stack_name,
                TemplateBody=template_body_json
            )
            return response
        except botocore.exceptions.ClientError as error:
            # Handle specific errors (e.g., network issues, permissions) or re-raise
            raise

    def describe(self):
        """
        Checks the status of the stack managed by this instance and returns the status and a message.
        """
        try:
            response = self.cf_client.describe_stacks(
                StackName=self.stack_name
            )
            status = response['Stacks'][0]['StackStatus']
            if status in ['CREATE_COMPLETE', 'UPDATE_COMPLETE']:
                message = "Stack update or creation complete."
            else:
                message = "Stack is in process or has an issue."
            return status, message
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'ValidationError':
                message = f"An error occurred (ValidationError) when calling the DescribeStacks operation: Stack with id {self.stack_name} does not exist"
                return None, message
            else:
                raise

    def delete(self):
        """
        Deletes the stack managed by this instance.
        """
        response = self.cf_client.delete_stack(
            StackName=self.stack_name
        )
        return response

    def update(self, template_body_json):
        """
        Updates the stack managed by this instance.

        :param template_body_json: JSON-formatted string of the new template body.
        """
        try:
            response = self.cf_client.update_stack(
                StackName=self.stack_name,
                TemplateBody=template_body_json
            )
            return response
        except botocore.exceptions.ClientError as error:
            error_message = error.response['Error']['Message']
            if "No updates are to be performed." in error_message:
                return {"message": "No updates are to be performed on the stack. It is already up-to-date."}
            elif "is in DELETE_IN_PROGRESS state and can not be updated" in error_message:
                return {"message": "The stack is currently being deleted and cannot be updated."}
            elif "is in CREATE_IN_PROGRESS state and can not be updated" in error_message:
                return {"message": "The stack is currently being created and cannot be updated."}
            else:
                raise




if __name__ == '__main__':
    cf_client = boto3.client('cloudformation')
    stack_name = 'my-new-stack'
    stack = Stack(cf_client, stack_name)

    # Prepare the template
    template_body = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {
            "MyS3Bucket": {
                "Type": "AWS::S3::Bucket"
            }
        }
    }
    template_body_json = json.dumps(template_body)

    # Example usage (uncomment to use)
    # Create stack
    response = stack.create(template_body_json)
    #print(response)

    # Check stack status
    status, message = stack.describe()
    print(f"Stack status: {status}\n{message}")

    # Update stack (Assuming the template_body or template_body_json has been modified appropriately)
    response = stack.update(template_body_json)
    #print(response)

    # Delete stack
    response = stack.delete()
    #print(response)
