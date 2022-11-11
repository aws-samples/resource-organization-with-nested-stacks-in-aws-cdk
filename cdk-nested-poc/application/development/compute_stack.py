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
        
        #Defining Lambda function which will make initial processing for the flow in Step Function
        self.preprocessing_lambda = lambda_.Function(self, "ETLInitialProcessing",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.InlineCode("print 'This Lambda is making initial type recognition and preprocessing'"),
            vpc=network.vpc,
            role = iam_role.lambda_role
        )
        
        #Defining Lambda function which will process CustomerID in Step Function
        self.customer_id_lambda = lambda_.Function(self, "ETLCustomerID",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.InlineCode("print 'This Lambda works with CustomerID'"),
            vpc=network.vpc,
            role = iam_role.lambda_role        
        )        
        
        #Defining Lambda function which will process OrderID in Step Function
        self.order_id_lambda = lambda_.Function(self, "ETLOrderID",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.InlineCode("print 'This Lambda works with OrderID'"),
            vpc=network.vpc,
            role = iam_role.lambda_role        
        )       

        #Defining Lambda function which will process Misc items in Step Function        
        self.misc_item_lambda = lambda_.Function(self, "ETLMiscItem",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.InlineCode("print 'This Lambda works with remaining items'"),
            vpc=network.vpc,
            role = iam_role.lambda_role        
        )        
             
                

        
