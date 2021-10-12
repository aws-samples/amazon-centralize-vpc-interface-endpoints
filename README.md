## Centralize access using VPC interface endpoints to access AWS services across multiple VPCs

Security and cost are always a top priority for AWS customers when designing their network. Amazon Virtual Private Cloud (Amazon VPC),  and it’s related networking components, offer many tools for implementing network connectivity. One such tool is VPC endpoints. Powered by AWS PrivateLink, VPC endpoints are private connections between your VPC and another AWS service without sending traffic over the internet, through a NAT instance, a VPN connection, or AWS Direct Connect. In this blog post, I present hub and spoke design where all the spoke VPCs use an interface VPC endpoint provisioned inside the hub (shared services) VPC. This architecture may help reduce the cost and maintenance for multiple interface VPC endpoints across different VPCs.

This code has been created to compliment the blog https://aws.amazon.com/blogs/networking-and-content-delivery/centralize-access-using-vpc-interface-endpoints/

## Installation

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
pip install -r requirements.txt
```

Once the environment has been configured, modify the app.py file to change/add any additiional VPC Endpoints you would like, e.g. if you wanted the VPC Endpoints for AWS Systems Manager

```
services =  ["ssm","ec2messages","ec2","ssmmessages","kms"]
```

At this point you can now synthesize the CloudFormation template for this code.

```
cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Deployment
To install the Services **Hub** VPC Cloudformation Template, use the following command with these parameters (with the Hub Credentials):
* VPCId = VPC to install the VPC Endpoints
* OrgCIDR = CIDR range for the Security Group on the VPC Endpoint (which IPs in your Org are allowed to use the Endpoints)
* EndpointSubnetIdList = Subnets where the VPC Endpoints should be installed, minimum 2 is recommended
* OrgID = Used to determine which accounts are allowed to Assume the Role and Authenticate VPCs to the Route53 Private Hosted Zone (PHZ)

```
cdk deploy <Stack-Name> --parameters VPCId=vpc-xxxxxxxxx \
   --parameters OrgCIDR=xx.xx.xx.xx/xx \
   --parameters EndpointSubnetIdList="subnet-xxxxxxxxx, subnet-xxxxxxxxxx, subnet-xxxxxxx"  \
   --parameters OrgID=o-xxxxxxxxxx
```

To install the Services **Spoke** VPC Cloudformation Template, use the following command with these parameters (with the Spoke Credentials):
* VPCId = VPC to associate to the Hub's PHZ 
* R53HubRoleToAssume = Route53 Hub Role to Assume for Authenticating the VPC against the PHZ, provided from the output of the Hub
* Route53DomainIDFor<Service1> = Route53 PHZ Domain ID to Authenticate and Associate against, 1 per Servuce, provided from the output of the Hub
```
cdk deploy <Stack-Name> --parameters VPCId=vpc-xxxxxxxxx \
  --parameters R53HubRoleToAssume=arn:aws:iam::xxxxxxxxxxxx:role/xxxxxxxxxxxx \
  --parameters Route53DomainIDFor<Service1>=xxxxxxxxxxxxxxxxxxxxx \
  --parameters Route53DomainIDFor<Service2>=xxxxxxxxxxxxxxxxxxxxx, etc.
```  
### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
