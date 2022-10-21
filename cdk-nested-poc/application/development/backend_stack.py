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
        
        ec2.Instance(self, "BackEndInstance1",
            vpc=network.vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.SMALL),
            machine_image=ec2.AmazonLinuxImage()
        )
        
        ec2.Instance(self, "BackEndInstance2",
            vpc=network.vpc,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.SMALL),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            )
        )
                

        
