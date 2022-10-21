from aws_cdk import (
    aws_lambda as lambda_,
    NestedStack
)
from constructs import Construct
from application.networking.vpc_stack import VPCStack
from application.security.iam_stack import IAMRoles




class ComputeStack(NestedStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        cidr,
        max_azs,        
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)        
        
        #Using Nested stacks from Security and Networking teams
        network = VPCStack(self, "NetworkStack", cidr=cidr, max_azs=max_azs,)
        iam_role = IAMRoles(self, "IAMRoles")  
        
        self.preprocessing_lambda = lambda_.Function(self, "ETLInitialProcessing",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.InlineCode("print 'This Lambda is making initial type recognition and preprocessing'"),
            vpc=network.vpc,
            role = iam_role.lambda_role
        )
        
        self.customerid_lambda = lambda_.Function(self, "ETLCustomerID",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.InlineCode("print 'This Lambda works with CustomerID'"),
            vpc=network.vpc,
            role = iam_role.lambda_role        
        )        
        
        self.orderid_lambda = lambda_.Function(self, "ETLOrderID",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.InlineCode("print 'This Lambda works with OrderID'"),
            vpc=network.vpc,
            role = iam_role.lambda_role        
        )       
        
        self.miscitem_lambda = lambda_.Function(self, "ETLMiscItem",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.InlineCode("print 'This Lambda works with remainging items'"),
            vpc=network.vpc,
            role = iam_role.lambda_role        
        )        
             
                

        
