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
    aws_ec2 as ec2,
    Stack
)
from constructs import Construct
from application.networking.vpc_stack import VPCStack

class BackEndStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)        
        
        #Using Nested stacks from Security and Networking teams
        network = VPCStack(self, "NetworkStackBackEnd", cidr='15.0.0.0/16', max_azs=1,)
        
        #Defining first EC2 instance
        ec2.Instance(self, "BackEndInstance1",
            vpc=network.vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.SMALL),
            machine_image=ec2.AmazonLinuxImage()
        )
        
        #Defining second EC2 instance
        ec2.Instance(self, "BackEndInstance2",
            vpc=network.vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.SMALL),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            )
        )
                

        
