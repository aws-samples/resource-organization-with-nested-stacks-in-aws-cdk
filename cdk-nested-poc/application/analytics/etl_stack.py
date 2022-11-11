# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from aws_cdk import (
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    Stack
)
from constructs import Construct
from application.development.compute_stack import ComputeStack



class ETLStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)        
        
        #Using Nested stacks from other teams and specifying the parameters we need
        compute = ComputeStack(self, "ComputeStack", cidr='10.0.0.0/16', max_azs=2)


        #Defining tasks for StepFunctions workflow
        starting_job = tasks.LambdaInvoke(self, "ETLInitialProcessing", lambda_function=compute.preprocessing_lambda)
        
        choice = sfn.Choice(self, "OrderID or CustomerID")
        
        #Using Lambda functions which were created by Development team in compute_stack.py
        handle_order_id_item = tasks.LambdaInvoke(self, "ETLCustomerID", lambda_function=compute.customer_id_lambda)
        handle_customer_id_item = tasks.LambdaInvoke(self, "ETLOrderID", lambda_function=compute.order_id_lambda)
        handle_other_item = tasks.LambdaInvoke(self, "ETLMiscItem", lambda_function=compute.misc_item_lambda)
               
        #Describing conditional block 
        choice.when(sfn.Condition.string_equals("$.type", "OrderID"), handle_order_id_item)
        choice.when(sfn.Condition.string_equals("$.type", "CustomerID"), handle_customer_id_item)
        choice.otherwise(handle_other_item)

        sfn_task_definition = starting_job.next(choice)
        
        #Defining State Machine of StepFunctions
        state_machine = sfn.StateMachine(self, "DemoStateMachine", definition=sfn_task_definition)            
        
                
