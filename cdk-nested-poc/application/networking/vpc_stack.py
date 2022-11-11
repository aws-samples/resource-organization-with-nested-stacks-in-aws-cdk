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
    aws_ec2 as ec2,
    NestedStack
)

class VPCStack(NestedStack):

    def __init__(
        self,
        scope: Construct,
        id: str,
        cidr,
        max_azs,          
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        #Defining VPC network with 2 subnets - private and public 
        self.vpc = ec2.Vpc(
            self, 'ProdStack',
            ip_addresses=ec2.IpAddresses.cidr(cidr),
            max_azs=max_azs,
            subnet_configuration=[
                {
                    'cidrMask': 28,
                    'name': 'public',
                    'subnetType': ec2.SubnetType.PUBLIC
                },
                {
                    'cidrMask': 28,
                    'name': 'private',
                    'subnetType': ec2.SubnetType.PRIVATE_WITH_EGRESS
                }
            ]
        )
