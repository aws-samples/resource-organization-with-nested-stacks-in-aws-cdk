#!/usr/bin/env python3
import os

import aws_cdk as cdk
from application.analytics.etl_stack import ETLStack
from application.development.backend_stack import BackEndStack

env_prod = cdk.Environment(account="557700951461", region="us-east-1")
env_stage = cdk.Environment(account="557700951461", region="us-west-2")

app = cdk.App()
#Creating the whole application based on Nested stacks
ETLStack(app, "ProductionDemo", env=env_prod)
BackEndStack(app, "BackEndDemoEnv", env=env_prod)

app.synth()
