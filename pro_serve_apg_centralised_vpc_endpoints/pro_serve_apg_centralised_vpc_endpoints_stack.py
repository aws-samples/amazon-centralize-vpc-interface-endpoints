from typing import List
from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_logs as logs,
)


from aws_cdk.custom_resources import (
    AwsCustomResource,
    AwsCustomResourcePolicy,
    PhysicalResourceId,
    AwsSdkCall,
)
import aws_cdk.custom_resources as custom_resources
import jsii


class ProServeApgCentralisedVpcEndpointsHubStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, services, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_id = core.CfnParameter(
            self,
            "VPCId",
            description="The VPC where you want to place the endpoints",
            type="AWS::EC2::VPC::Id",
            allowed_pattern="^vpc-.*$",
        ).value_as_string

        org_cidr = core.CfnParameter(
            self,
            "OrgCIDR",
            description="The CIDR range that requests can originate from to use this endpoint.",
            allowed_pattern="^[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\/[\d]{1,3}$",
            constraint_description="CIDR should be in form X.X.X.X/X",
        ).value_as_string

        org_id = core.CfnParameter(
            self,
            "OrgID",
            description="The Organization ID which you'll allow to associate with your Hosted Zone",
            allowed_pattern="^o-[a-z0-9]{10,32}",
        ).value_as_string

        subnet_ids = core.CfnParameter(
            self,
            "EndpointSubnetIdList",
            type="List<AWS::EC2::Subnet::Id>",
            description="The subnets to insert VPC endpoints into",
            min_length=1,
            allowed_pattern="^subnet-.*$",
        ).value_as_list

        vpc = ec2.Vpc.from_vpc_attributes(
            self, "EndpointVPC", vpc_id=vpc_id, availability_zones=core.Fn.get_azs(core.Aws.REGION)
        )

        security_group_for_endpoints = ec2.SecurityGroup(self, "SecurityGroupForEndpoints", vpc=vpc)

        security_group_for_endpoints.add_ingress_rule(
            ec2.Peer.ipv4(org_cidr),
            connection=ec2.Port(protocol=ec2.Protocol.TCP, from_port=443, to_port=443, string_representation="TTA"),
        )

        # Create a Role that is assumed by the Spoke
        r53_role = iam.Role(
            self,
            "R53 Role",
            assumed_by=iam.AnyPrincipal().with_conditions({"StringEquals": {"aws:PrincipalOrgID": org_id}}),
        )

        # Add permissions to the Role
        r53_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=["*"],
                actions=["route53:CreateVPCAssociationAuthorization", "route53:DeleteVPCAssociationAuthorization"],
            )
        )

        # The list of services are in the app.py file
        for service in services:
            record_name = f"{service}.{core.Aws.REGION}.amazonaws.com"

            endpoint = ec2.CfnVPCEndpoint(
                self,
                f"EndpointFor{service}",
                vpc_id=vpc_id,
                security_group_ids=[security_group_for_endpoints.security_group_id],
                vpc_endpoint_type="Interface",
                private_dns_enabled=False,
                service_name=f"com.amazonaws.{core.Aws.REGION}.{service}",
                subnet_ids=subnet_ids,
            )

            hosted_zone = route53.PrivateHostedZone(self, f"PrivateZoneFor{service}", zone_name=record_name, vpc=vpc)
            route53.RecordSet(
                self,
                f"AliasRecordFor{service}",
                record_type=route53.RecordType.A,
                zone=hosted_zone,
                record_name=record_name,
                target=route53.RecordTarget(
                    alias_target=RemoteInterfaceEndpointTarget(core.Fn.select(0, endpoint.attr_dns_entries))
                ),
            )

            core.CfnOutput(self, f"Route53DomainIDFor{service.upper()}", value=hosted_zone.hosted_zone_id)
        core.CfnOutput(self, f"R53HubRoleToAssume", value=r53_role.role_arn)


class ProServeApgCentralisedVpcEndpointsSpokeStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, services: List, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_id = core.CfnParameter(
            self,
            "VPCId",
            description="The VPC that you want to use the centralised endpoints in.",
            type="AWS::EC2::VPC::Id",
            allowed_pattern="^vpc-.*$",
        ).value_as_string

        assume_role_arn = core.CfnParameter(
            self,
            f"R53HubRoleToAssume",
            description=f"The Route53 Role in the Hub Account that allows us to Authorize a VPC to the Private Hosted Zone",
            allowed_pattern="^arn:aws:iam::[\d]{12}:role/.*$",
        ).value_as_string

        # R53Lambda Role
        associate_vpc_lambda_role = iam.Role(
            self, "associate_vpc_lambda_role", assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        associate_vpc_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        associate_vpc_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole")
        )

        # Add permissions to the Lambda Role for R53 and AssumeRole
        associate_vpc_lambda_role.add_to_policy(
            iam.PolicyStatement(effect=iam.Effect.ALLOW, resources=["*"], actions=["ec2:DescribeVpcs"])
        )
        associate_vpc_lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=[
                    "arn:aws:route53:::hostedzone/*",
                    f"arn:aws:ec2:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:vpc/{vpc_id}",
                ],
                actions=["route53:AssociateVPCWithHostedZone", "route53:DisassociateVPCFromHostedZone"],
            )
        )

        # Add permissions to the Lambda Role for Assume Role
        associate_vpc_lambda_role.add_to_policy(
            iam.PolicyStatement(effect=iam.Effect.ALLOW, resources=[assume_role_arn], actions=["sts:AssumeRole"])
        )

        R53_Lambda = _lambda.Function(
            self,
            f"R53AuthenticateAssociateVPC",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset("lambda"),
            handler="R53Associate.handler",
            role=associate_vpc_lambda_role,
        )
        provider_for_r53_lambda = custom_resources.Provider(
            self,
            "Provider_For_R53_Lambda",
            on_event_handler=R53_Lambda,
            log_retention=logs.RetentionDays.ONE_DAY,  # default is INFINITE
        )

        # The list of services are in the app.py file
        for service in services:
            service_HostedZoneID = core.CfnParameter(
                self,
                f"Route53DomainIDFor{service.upper()}",
                description=f"The route53 hosted zone id from the hub stack for the the {service.upper()} service, the string before the colon in <route53 hosted zone id>:<regional vpc endpoint dns name>",
                allowed_pattern="^[A-Z0-9]{1,32}$",
            ).value_as_string

            core.CustomResource(
                self,
                f"R53AssociateCustomResourceFor{service.upper()}",
                service_token=provider_for_r53_lambda.service_token,
                properties={
                    "VPCID": vpc_id,
                    "HostedZoneID": service_HostedZoneID,
                    "AccountID": core.Aws.ACCOUNT_ID,
                    "RoleARN": assume_role_arn,
                },
            )


@jsii.implements(route53.IAliasRecordTarget)
class RemoteInterfaceEndpointTarget:
    def __init__(self, remote_endpoint_config):
        """:param: remote_endpoint_config is a key value pair in the form of <hosted zone id>:<vpc endpoint dns name of the record>"""
        self.remote_endpoint_config = remote_endpoint_config

    def bind(self, _, _a):
        return route53.AliasRecordTargetConfig(
            dns_name=cdk.Fn.select(1, cdk.Fn.split(":", self.remote_endpoint_config)),
            hosted_zone_id=cdk.Fn.select(0, cdk.Fn.split(":", self.remote_endpoint_config)),
        )
