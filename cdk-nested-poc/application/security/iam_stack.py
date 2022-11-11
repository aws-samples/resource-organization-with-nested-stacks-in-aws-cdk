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


from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    NestedStack
)

class IAMRoles(NestedStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)
        
        #Creating required IAM role, which will be attached to Lambda functions
        self.lambda_role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role to be used by Lambda"
        )

        #Attaching IAM Policies to the role above, so Lambda functions can be executed and run within VPC Network
        self.lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        self.lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
