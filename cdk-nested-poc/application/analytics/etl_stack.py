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
        
        handle_orderid_item = tasks.LambdaInvoke(self, "ETLCustomerID", lambda_function=compute.customerid_lambda)
        handle_customerid_item = tasks.LambdaInvoke(self, "ETLOrderID", lambda_function=compute.orderid_lambda)
        handle_other_item = tasks.LambdaInvoke(self, "ETLMiscItem", lambda_function=compute.miscitem_lambda)
               
       
        choice.when(sfn.Condition.string_equals("$.type", "OrderID"), handle_orderid_item)
        choice.when(sfn.Condition.string_equals("$.type", "CustomerID"), handle_customerid_item)
        choice.otherwise(handle_other_item)

        sfn_task_definition = starting_job.next(choice)
        
        #Defining State Machine of StepFunctions
        state_machine = sfn.StateMachine(self, "DemoStateMachine", definition=sfn_task_definition)            
        
                
