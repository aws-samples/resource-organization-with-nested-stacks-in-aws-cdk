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

        self.vpc = ec2.Vpc(
            self, 'ProdStack',
            cidr=cidr,
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
                    'subnetType': ec2.SubnetType.PRIVATE_WITH_NAT
                }
            ]
        )
