from typing import List
from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_lambda as _lambda,
    aws_iam as iam
)


from aws_cdk.custom_resources import (
    AwsCustomResource,
    AwsCustomResourcePolicy,
    PhysicalResourceId,
    AwsSdkCall
)
import jsii


class ProServeApgCentralisedVpcEndpointsHubStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, services, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_id = core.CfnParameter(self, "VPCId",description="The VPC where you want to place the endpoints", type="AWS::EC2::VPC::Id").value_as_string

        org_cidr = core.CfnParameter(
            self, "OrgCIDR", description="The CIDR range that requests can originate from to use this endpoint.", allowed_pattern="^[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\/[\d]{1,3}$", constraint_description="CIDR should be in form X.X.X.X/X",
        ).value_as_string

        subnet_ids = core.CfnParameter(
            self, "EndpointSubnetIdList", type="List<AWS::EC2::Subnet::Id>", description="The subnets to insert VPC endpoints into", min_length=1
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
        R53_role = iam.Role(self, "R53 Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # Add permissions to the Role
        R53_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["route53:CreateVPCAssociationAuthorization","route53:DeleteVPCAssociationAuthorization"]
        ))


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
            
            hosted_zone = route53.PrivateHostedZone(
                self, 
                f"PrivateZoneFor{service}",
                zone_name=record_name,
                vpc=vpc
            )
            route53.RecordSet(
                self,
                f"AliasRecordFor{service}",
                record_type=route53.RecordType.A,
                zone=hosted_zone,
                record_name=record_name,
                target=route53.RecordTarget(alias_target=RemoteInterfaceEndpointTarget(core.Fn.select(0, endpoint.attr_dns_entries))),
            )

            core.CfnOutput(self, f"Route53Domainfor{service}", value=core.Fn.select(0, endpoint.attr_dns_entries))


class ProServeApgCentralisedVpcEndpointsSpokeStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, services: List, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_id = core.CfnParameter(self, "VPCId",description="The VPC that you want to use the centralised endpoints in.", type="AWS::EC2::VPC::Id").value_as_string
        AssumeRoleARN = core.CfnParameter(
            self,
            f"AssumeRoleARN",
            description=f"The Route53 Role in the Hub Account that allows us to Authorize a VPC to the Private Hosted Zone",
#            allowed_pattern="/^arn:aws:iam::([0-9]+):.+)$"
        ).value_as_string

        vpc = ec2.Vpc.from_vpc_attributes(
            self, "EndpointVPC", vpc_id=vpc_id, availability_zones=core.Fn.get_azs(core.Aws.REGION)
        )

        # We forcefully create a role for the 
        # Create a Role that is assumed by the Spoke
        R53_Spoke_role = iam.Role(self, "R53 Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # Add permissions to the Role
        R53_Spoke_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["*"]
        ))
        R53_Spoke_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        R53_Spoke_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))

        for service in services:

            service_HostedZoneID = core.CfnParameter(
                self,
                f"Route53HostedZoneID{service.upper()}",
                description=f"The route53 hosted zone id from the hub stack for the the {service.upper()} service, the string before the colon in <route53 hosted zone id>:<regional vpc endpoint dns name>",
                allowed_pattern="^[A-Z0-9]+$"
            ).value_as_string

            record_name = f"{service}.{core.Aws.REGION}.amazonaws.com"
            vpc_association_authorization = AwsCustomResource(self, f"VpcAssociationAuthorization-{service}",
                on_create={
                    "assumed_role_arn": "arn:aws:iam::610408810780:role/ProServeApgCentralisedVpcEndpoints-R53Role778AB903-DK5I6NEW48MZ",
                    "service": "Route53",
                    "action": "createVPCAssociationAuthorization",
                    "parameters": {
                        "HostedZoneId": "Z044055532752CKAOB9Z7",
                        "VPC": {
                            "VPCId": vpc_id,
                            "VPCRegion": core.Aws.REGION
                        }
                    },
                    "physical_resource_id": PhysicalResourceId.of(f"createVPCAssociationAuthorization-{service}") #Used as Role SessionName so must be less that <64 chars
                },                           
                # Will ignore any resource and use the assumedRoleArn as resource and 'sts:AssumeRole' for service:action
#                policy=AwsCustomResourcePolicy.from_sdk_calls(resources=AwsCustomResourcePolicy.ANY_RESOURCE)
                role=R53_Spoke_role,
                policy = AwsCustomResourcePolicy.from_statements(
                    statements=[
                        iam.PolicyStatement(
                            actions=["route53:*","ec2:*","sts:AssumeRole"], 
                            resources=["*"])
                            ]
                        )
            )
            ### awscustomresource does not like to in a row as it gets confused with the Roles/Permissions - so will create my own Lambda
                    lambda_role = iam.Role(self, "Lambda Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
            
        # Add permissions to the Lambda Role for R53 and AssumeRole
        lambda_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["sts:AssumeRole","route53:AssociateVPCWithHostedZone","route53:DisassociateVPCFromHostedZone"]
        ))

        R53_Lambda = _lambda.Function(
            self, 'R53Associate',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='R53Associate.handler',
            role=lambda_role
        )
        my_provider = cr.Provider(self, "MyProvider",
        on_event_handler=R53_Lambda,
        log_retention=logs.RetentionDays.ONE_DAY, # default is INFINITE
        )

        CustomResource(self, "Run my Lambda", 
            service_token=my_provider.service_token, 
            properties={
                "VPCID": vpc_id ,
                "HostedZoneID": service_HostedZoneID,
                "Action": "ASSOCIATE",
            },
        )



            # vpc_AssociateVPCWithHostedZone = AwsCustomResource(self, f"AssociateVPCWithHostedZone-{service}",
            #     on_create={
            #         "service": "Route53",
            #         "action": "associateVPCWithHostedZone",
            #         "parameters": {
            #             "HostedZoneId": "Z044055532752CKAOB9Z7",
            #             "VPC": {
            #                 "VPCId": vpc_id,
            #                 "VPCRegion": core.Aws.REGION
            #             }
            #         },
            #         "physical_resource_id": PhysicalResourceId.of(f"associateVPCWithHostedZone-{service}") #Used as Role SessionName so must be less that <64 chars
            #     },
            #     role=R53_Spoke_role,
            #     policy = AwsCustomResourcePolicy.from_statements(
            #         statements=[
            #             iam.PolicyStatement(
            #                 actions=["route53:*","ec2:*"], 
            #                 resources=["*"])
            #                 ]
            #             )
            # )
            # vpc_AssociateVPCWithHostedZone.node.add_dependency(vpc_association_authorization)
            # vpc_AssociateVPCWithHostedZone.node.add_dependency(R53_Spoke_role)

            # # Best Practise is to remove the Authorisation afterwards
            # vpc_association_authorization = AwsCustomResource(self, f"deleteVPCAssociationAuthorization-{service}",
            #     on_create={
            #         "assumed_role_arn": "arn:aws:iam::610408810780:role/ProServeApgCentralisedVpcEndpoints-R53Role778AB903-DK5I6NEW48MZ",
            #         "service": "Route53",
            #         "action": "deleteVPCAssociationAuthorization",
            #         "parameters": {
            #             "HostedZoneId": service_HostedZoneID,
            #             "VPC": {
            #                 "VPCId": vpc_id,
            #                 "VPCRegion": core.Aws.REGION
            #             }
            #         },
            #         "physical_resource_id": PhysicalResourceId.of(f"deleteVPCAssociationAuthorization-{service}") #Used as Role SessionName so must be less that <64 chars
            #     },                           
            #     # Will ignore any resource and use the assumedRoleArn as resource and 'sts:AssumeRole' for service:action
            #     policy=AwsCustomResourcePolicy.from_sdk_calls(resources=AwsCustomResourcePolicy.ANY_RESOURCE)
            # )            
            # vpc_AssociateVPCWithHostedZone.node.add_dependency(vpc_association_authorization)


@jsii.implements(route53.IAliasRecordTarget)
class RemoteInterfaceEndpointTarget:
    def __init__(self, remote_endpoint_config):
        """ :param: remote_endpoint_config is a key value pair in the form of <hosted zone id>:<vpc endpoint dns name of the record>
    """
        self.remote_endpoint_config = remote_endpoint_config

    def bind(self, _, _a):

        return route53.AliasRecordTargetConfig(
            dns_name=cdk.Fn.select(1, cdk.Fn.split(":", self.remote_endpoint_config)),
            hosted_zone_id=cdk.Fn.select(0, cdk.Fn.split(":", self.remote_endpoint_config)),
        )

