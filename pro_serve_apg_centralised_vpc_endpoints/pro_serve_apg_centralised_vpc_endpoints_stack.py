from typing import List
from aws_cdk import core as cdk

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_route53 as route53,
    aws_route53_targets as targets,
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

        for endpoint_name in services:

            endpoint = ec2.CfnVPCEndpoint(
                self,
                f"EndpointFor{endpoint_name}",
                vpc_id=vpc_id,
                security_group_ids=[security_group_for_endpoints.security_group_id],
                vpc_endpoint_type="Interface",
                private_dns_enabled=True,
                service_name=f"com.amazonaws.{core.Aws.REGION}.{endpoint_name}",
                subnet_ids=subnet_ids,
            )

            core.CfnOutput(self, f"Route53Domainfor{endpoint_name}", value=core.Fn.select(0, endpoint.attr_dns_entries))


class ProServeApgCentralisedVpcEndpointsSpokeStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, services: List, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_id = core.CfnParameter(self, "VPCId",description="The VPC that you want to use the centralised endpoints in.", type="AWS::EC2::VPC::Id").value_as_string

        vpc = ec2.Vpc.from_vpc_attributes(
            self, "EndpointVPC", vpc_id=vpc_id, availability_zones=core.Fn.get_azs(core.Aws.REGION)
        )

        for service in services:

            service_target_record = core.CfnParameter(
                self,
                f"Route53RecordOuputFor{service.upper()}",
                description=f"The output from the hub stack for the the {service.upper()} service, in the for of <route53 hosted zone id>:<regional vpc endpoint dns name>",
                allowed_pattern="^[A-Z0-9]+:.+$"
            ).value_as_string

            record_name = f"{service}.{core.Aws.REGION}.amazonaws.com"
            hosted_zone = route53.HostedZone(self, f"PrivateZoneFor{service}", zone_name=record_name, vpcs=[vpc])

            route53.RecordSet(
                self,
                f"AliasRecordFor{service}",
                record_type=route53.RecordType.A,
                zone=hosted_zone,
                record_name=record_name,
                target=route53.RecordTarget(alias_target=RemoteInterfaceEndpointTarget(service_target_record)),
            )


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

