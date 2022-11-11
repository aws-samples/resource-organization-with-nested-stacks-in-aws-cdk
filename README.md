# Resource organization with nested stacks in the AWS CDK


This GitHub repository contains resources to deploy the solution described in the [Resource organization with nested stacks in the AWS CDK](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk)

When customers start their cloud journey, they start with manual console actions and scripting CLI automations, but then face challenges scaling these approaches to more complex architectures, to multiple accounts, or across regions. The [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html) uses familiar programming languages to provision resources in a safe, repeatable manner as a layer of abstraction on top of [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html). It also allows you to compose and share your own custom constructs incorporating your organization's business and technical requirements, helping you and your teammates expedite new projects. In some cases, teams can manage their infrastructure by using a monolithic stack which defines the whole infrastructure. Single dedicated DevOps team can be owner of this stack and provide necessary maintenance of it.  However, managing big enterprise infrastructure poses new challenges, in terms of change management, cross-team development and reusability, especially if multiple teams are involved there. Multi-layered responsibility model in enterprise organization adds even more complexity there.


Managing [Nested Stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html) using AWS CDK addresses such kind of concerns. DevOps teams and Solution Architects who are working with complex and rapidly growing stacks can define usage of nested stacks in their operational workflow. The walkthrough will show the example of organizing work for combination of two common frameworks: a multi-layered architecture and service-oriented architecture (SOA) of the infrastructure in a typical IT department.

## Overview of the Solution

As your infrastructure grows, common patterns can emerge in which you declare the same components in multiple templates. You can separate out these common components and create dedicated templates for them. Then use the resource in your template to reference other templates, creating nested stacks. This is a best practice for well-organized IT department in enterprise company – each team owns and responsible of their own part of the infrastructure or logical unit.

This solution shows example of interaction of 4 different teams in the enterprise organization, which are involved in common application development and which are defining their system by using Infrastructure as a Code (IAC) approach. It is great for keeping your resources organized and have ability to reproduce or restore the whole stack if needed. It is also simpler to organize contribution of the code for the whole team if the infrastructure defined as a code, so there could be added version control system, like [AWS CodeCommit](https://aws.amazon.com/codecommit/), GitHub and etc.

CDK Nested Stacks are great when you want to separate logical resources in your stack and reference those resources in other nested stacks.

By using CDK Nested Stacks each team can work separately from each other, and in the same time effectively reuse stacks from each other.

To give some more visibility for the walkthrough, we will also define 4 teams, which usually exist in IT department:
* **Networking team** – this team is responsible for defining network connectivity in the cloud. In real world organization this could be an Operational team or dedicated NetOps team 
* **Security team** – this could be a department under CSO office, who is responsible for reducing security threats, granting access to the resources and implementing security best practices.
* **Development team** – in this walkthrough, this team is responsible for 2 different workflows: developing code for processing incoming data of digital orders and supporting backend components for it. In real world this could be any Dev team working with data processing, ETL, business logic implementation, etc. In most cases, infrastructure, which Dev team is using, requires network to be based on (in this example, provided by Networking team) and access to the infrastructure (provided by Security team)
* **Analytics team** – in our case this team is building high-level ETL logic by using components \ workers, provided by Development team.

Organization from this example represents both a multi-layered architecture and service-oriented architecture (SOA): Development team and Analytics team are working independently on different services (ETL and Backend) – this represents SOA architecture pattern. And in the same time, Security, Networking and Development/Analytics teams are working independently on different levels of infrastructure abstraction – this represents multi-layered architecture.

The benefit of this approach is that all teams can work independently, they can define their own deadlines, have their own sprints and in case of issues – each the teams can fix their own part of the infrastructure without affecting development process for other teams.

Below you can find the architectural diagram of the relationship between stacks and teams. The diagram is separated vertically by department layer, and each of the stack belongs to a different team, which is developing components of the stack.

![architectural diagram](/images/diagram.png)


## Prerequisites

In this walkthrough we will be creating a Nested Stack in AWS CloudFormation by using CDK. Here is a list of requirements for deploying this POC:

1. Coding environment, which has access to AWS and where you will be executing CDK commands and writing the code. It could be [AWS Cloud9](https://aws.amazon.com/cloud9/) or any other consoles or terminals where you can install AWS CDK.
2. Basic knowledge of one of the programming languages, which are supported by AWS CDK: JavaScript, TypeScript, Python, Java, C# and Go. In this walkthrough will be shown example, written in Python.
3. You need also to grant your AWS User privilege to create, read, modify and remove resources in AWS account. In our exercise we will be working with such resources:
    - EC2
    - Lambda
    - IAM
    - VPC
    - Step Functions
You can get full list of required permissions per AWS service in this file - [permissions.txt](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/permissions.txt)
In this file you can find the full name of the actions, which are required for spefic service. You need to add these permissions as inline policy or attached policy to your user’s role in AWS Account.
Here is an example:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
                "Action": [
                "states:CreateActivity",
                "states:UpdateStateMachine",
                "states:DeleteStateMachine",
                "states:DeleteActivity",
                "states:CreateStateMachine"
                ],   
            "Resource": "*" 
        }
    ]
}
```

You can find more information about access policies in our documentation: [Creating IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html)

4. AWS Cloud Development Kit (CDK) v.2.50.0 or higher. 

You can check if you have CDK installed in your environment by running command:

`cdk —-version`

You should receive output similar to this:

![cdk version](/images/cdk_version.png)

If you don’t have CDK installed or version is lower than 2.50.0, please follow this guide to [install](https://docs.aws.amazon.com/cdk/v2/guide/getting\_started.html) or [upgrade](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html) your CDK. 

You might also need to bootstrap your AWS Account if you didn’t use it previously for CDK. You can do this by running command cdk bootstap.  More information about bootstapping for AWS CDK is in our [documentation here](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html).

## Walkthrough

As initial step you need to initiate the CDK project in a fresh folder. You can do this by running the command below from this folder:

`cdk init app --language=python`

and also, you need to update Python libraries which are required for CDK by using this command: 

`pip install -r requirements.txt`


Then you should receive the initialization response:

![cdk initialization](/images/cdk_initialization.png)

The last command has initiated the folder structure for you project. Right now, the project is empty, so we need to add code and templates inside. We will create 5 different stacks which are being owned by separate teams to be able to create an application. As was mentioned previously, most of the IT departments are working within their own workspaces, for example repositories, folders, infrastructure. In most cases this is done to prevent cross-blocking and control issues. In our example we will also be representing similar case, where each team is supposed to be working in its own folder, however stacks will be separated in different files within the folder to simplify development process.

To avoid mistakes, it is recommended to clone the whole repo from our [GitHub repository](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk) and copy its content to the folder, where you initiated your CDK project. Run the command from below in your folder, where you downloaded the repository and replace `<path_where_cdk_was_initiated>` with the path where CDK Project was initiated:

`cp -fr cdk-nested-poc/* <path_where_cdk_was_initiated>/`


## Defining nested stack for Networking team

The Networking team is responsible for defining the network configuration, which can be used by other teams in the company. Here, we will be deploying [VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html), [Subnets](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html), [NAT Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html), [Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html) and other network components, required for building compute services into the pre-defined networking structure.

The code for the VPC stack should be placed in path `application/networking/vpc_stack.py`. Additionally put the `application/networking/__init__.py` to the same folder so CDK will recognize `vpc_stack.py` as [Construct](https://docs.aws.amazon.com/cdk/v2/guide/constructs.html). You can find the source of the code in GitHub page under the same path here: [vpc_stack.py](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/cdk-nested-poc/application/networking/vpc_stack.py) and [__init.py__](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/cdk-nested-poc/application/networking/__init__.py)


## Defining nested stack for Security team

The Security team is responsible for granting access to other teams, by managing [IAM users and roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id.html). This is a usual case for many Security teams and CSO office in organization.

The code for the IAM stack should be placed in path `application/security/iam_stack.py`. Additionally put the `application/security/__init__.py` to the same folder.
The source code can also be found in the GitHub under these links: [iam_stack.py](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/cdk-nested-poc/application/security/iam_stack.py) and [__init.py__](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/cdk-nested-poc/application/security/__init__.py)

## Defining nested stack for Development team 

Most customers have multiple teams developing different components of application. In our example, this Dev team will create 2 sub-components:

1. Reusable compute components for Analytics team, which is consists of 4 [Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) functions (Nested Stack)
2. Standalone Backend environment which is being used by the Dev team itself (Standalone Stack). The environment will consists of 2 [EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) instances 

There will be 2 files with a code for ComputeStack and BackEndStack. Code should be placed in `application/development/compute_stack.py` and `application/development/backend_stack.py` respectively. Additionally put the `application/development/__init__.py` to the same folder.

Link to [compute_stack.py](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/cdk-nested-poc/application/development/compute_stack.py)
Link to [backend_stack.py](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/cdk-nested-poc/application/development/backend_stack.py)
Link to [__init.py__](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/cdk-nested-poc/application/development/__init__.py)

## Defining root stack for Analytics team

We are using Analytics team in this example to define the high-level logic of processing customer orders. The compute coding was done previously by Dev team and defined by it in ComputeStack (4 Lambda functions). The task for Analytics team here is to define the processing algorithm in [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) by using ETLStack.

The code for the ETL stack should be placed in path `application/analytics/etl_stack.py`. Additionally put the `application/analytics/__init__.py` to the same folder.
Here you can find GitHub location of the [etl_stack.py](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/cdk-nested-poc/application/analytics/etl_stack.py) and [__init.py__](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/cdk-nested-poc/application/development/__init__.py)

## Defining the App as a collection of the underlying Stacks

Finally, we’ll deploy all of these stacks together by defining them in the app.py file, which the CDK uses to synthesize and then deploy the resources we’ve defined in our separate stacks as a single application. This file is already created during the `cdk init` command execution, so you need to replace its content with the one from GitHub repo - [app.py](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk/blob/main/cdk-nested-poc/app.py)

## Deploying to AWS

To deploy the application, which was developed by 4 different teams, you need to go to the top level folder, where you initiated the project, and start the deployment by using command `cdk deploy --all`

Since CDK is deploying security groups and IAM roles, you will be asked approval in the command line. Type y to approve and the deployment will be initialized.

![stack deployment](/images/deployment.png)

In the end of execution, you will have 2 CloudFormation stacks, and each of them contains Nested stacks from other teams:

![CloudFormation screen](/images/cloudformation_screen.png)

Also, you will be able to see new infrastructure, which was created by this CDK execution:

VPC

![VPC screen](/images/vpc_screen.png)

Lambda function

![Lambda screen](/images/lambda_screen.png)

AWS StepFunctions

![AWS StepFunctions screen](/images/stepfunctions_screen.png)

EC2 instances

![EC2 screen](/images/ec2_screen.png)

## Conclusion

In this post, we provided a solution that organizes an infrastructure development workflow where each team can develop their own part of infrastructure independently and contribute in development of the common application. With this solution, you can apply a similar pattern in your organization and reduce operational complexity in managing the cloud. This pattern can be applied to a multi-layered development workflow, service-oriented development workflow or to the mix of both. Use the CDK code in [this GitHub repo](https://github.com/aws-samples/resource-organization-with-nested-stacks-in-aws-cdk) to reproduce the framework and get started building your own applications more quickly

## Cleanup

Frugality is the one of the Amazon Leadership principles, so we recommend cleaning up unused infrastructure to limit costs that may be incurred over time. To remove the infrastructure you just created, you can either delete the stack which you created in AWS CloudFormation console, or run command `cdk destroy --all` from the folder, where you executed `cdk init` and `cdk deploy --all`

![Cleanup screen](/images/cleanup.png)

## Read more about AWS CDK and Resource management

* [AWS CDK API Reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html)
* [Share reusable infrastructure as code by using AWS CloudFormation modules and StackSets](https://aws.amazon.com/blogs/mt/share-reusable-infrastructure-code-aws-cloudformation-modules-and-stacksets/)
* [Best practices for developing cloud applications with AWS CDK](https://aws.amazon.com/blogs/devops/best-practices-for-developing-cloud-applications-with-aws-cdk/)
* [AWS CloudFormation best practices](https://aws.amazon.com/blogs/devops/best-practices-for-developing-cloud-applications-with-aws-cdk/)
* [AWS Blogs](https://aws.amazon.com/blogs/?awsf.blog-master-sector=*all&awsf.blog-master-security=*all&awsf.blog-master-storage=*all&awsf.blog-master-category=*all&awsf.blog-master-learning-levels=*all&awsf.blog-master-industry=*all&awsf.blog-master-analytics-products=*all&awsf.blog-master-artificial-intelligence=*all&awsf.blog-master-aws-cloud-financial-management=*all&awsf.blog-master-blockchain=*all&awsf.blog-master-business-applications=*all&awsf.blog-master-compute=*all&awsf.blog-master-customer-enablement=*all&awsf.blog-master-customer-engagement=*all&awsf.blog-master-database=*all&awsf.blog-master-developer-tools=*all&awsf.blog-master-devops=*all&awsf.blog-master-end-user-computing=*all&awsf.blog-master-mobile=*all&awsf.blog-master-iot=*all&awsf.blog-master-management-governance=*all&awsf.blog-master-media-services=*all&awsf.blog-master-migration-transfer=*all&awsf.blog-master-migration-solutions=*all&awsf.blog-master-networking-content-delivery=*all&awsf.blog-master-programming-language=*all)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

