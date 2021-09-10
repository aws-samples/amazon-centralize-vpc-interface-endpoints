'''
# AWS::GlobalAccelerator Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

## Introduction

AWS Global Accelerator (AGA) is a service that improves the availability and
performance of your applications with local or global users.

It intercepts your user's network connection at an edge location close to
them, and routes it to one of potentially multiple, redundant backends across
the more reliable and less congested AWS global network.

AGA can be used to route traffic to Application Load Balancers, Network Load
Balancers, EC2 Instances and Elastic IP Addresses.

For more information, see the [AWS Global
Accelerator Developer Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GlobalAccelerator.html).

## Example

Here's an example that sets up a Global Accelerator for two Application Load
Balancers in two different AWS Regions:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_globalaccelerator as globalaccelerator
import aws_cdk.aws_globalaccelerator_endpoints as ga_endpoints
import aws_cdk.aws_elasticloadbalancingv2 as elbv2

# Create an Accelerator
accelerator = globalaccelerator.Accelerator(stack, "Accelerator")

# Create a Listener
listener = accelerator.add_listener("Listener",
    port_ranges=[PortRange(from_port=80), PortRange(from_port=443)
    ]
)

# Import the Load Balancers
nlb1 = elbv2.NetworkLoadBalancer.from_network_load_balancer_attributes(stack, "NLB1",
    load_balancer_arn="arn:aws:elasticloadbalancing:us-west-2:111111111111:loadbalancer/app/my-load-balancer1/e16bef66805b"
)
nlb2 = elbv2.NetworkLoadBalancer.from_network_load_balancer_attributes(stack, "NLB2",
    load_balancer_arn="arn:aws:elasticloadbalancing:ap-south-1:111111111111:loadbalancer/app/my-load-balancer2/5513dc2ea8a1"
)

# Add one EndpointGroup for each Region we are targeting
listener.add_endpoint_group("Group1",
    endpoints=[ga_endpoints.NetworkLoadBalancerEndpoint(nlb1)]
)
listener.add_endpoint_group("Group2",
    # Imported load balancers automatically calculate their Region from the ARN.
    # If you are load balancing to other resources, you must also pass a `region`
    # parameter here.
    endpoints=[ga_endpoints.NetworkLoadBalancerEndpoint(nlb2)]
)
```

## Concepts

The **Accelerator** construct defines a Global Accelerator resource.

An Accelerator includes one or more **Listeners** that accepts inbound
connections on one or more ports.

Each Listener has one or more **Endpoint Groups**, representing multiple
geographically distributed copies of your application. There is one Endpoint
Group per Region, and user traffic is routed to the closest Region by default.

An Endpoint Group consists of one or more **Endpoints**, which is where the
user traffic coming in on the Listener is ultimately sent. The Endpoint port
used is the same as the traffic came in on at the Listener, unless overridden.

## Types of Endpoints

There are 4 types of Endpoints, and they can be found in the
`@aws-cdk/aws-globalaccelerator-endpoints` package:

* Application Load Balancers
* Network Load Balancers
* EC2 Instances
* Elastic IP Addresses

### Application Load Balancers

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
alb = elbv2.ApplicationLoadBalancer(...)

listener.add_endpoint_group("Group",
    endpoints=[
        ga_endpoints.ApplicationLoadBalancerEndpoint(alb,
            weight=128,
            preserve_client_ip=True
        )
    ]
)
```

### Network Load Balancers

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
nlb = elbv2.NetworkLoadBalancer(...)

listener.add_endpoint_group("Group",
    endpoints=[
        ga_endpoints.NetworkLoadBalancerEndpoint(nlb,
            weight=128
        )
    ]
)
```

### EC2 Instances

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
instance = ec2.instance(...)

listener.add_endpoint_group("Group",
    endpoints=[
        ga_endpoints.InstanceEndpoint(instance,
            weight=128,
            preserve_client_ip=True
        )
    ]
)
```

### Elastic IP Addresses

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
eip = ec2.CfnEIP(...)

listener.add_endpoint_group("Group",
    endpoints=[
        ga_endpoints.CfnEipEndpoint(eip,
            weight=128
        )
    ]
)
```

## Client IP Address Preservation and Security Groups

When using the `preserveClientIp` feature, AGA creates
**Elastic Network Interfaces** (ENIs) in your AWS account, that are
associated with a Security Group AGA creates for you. You can use the
security group created by AGA as a source group in other security groups
(such as those for EC2 instances or Elastic Load Balancers), if you want to
restrict incoming traffic to the AGA security group rules.

AGA creates a specific security group called `GlobalAccelerator` for each VPC
it has an ENI in (this behavior can not be changed). CloudFormation doesn't
support referencing the security group created by AGA, but this construct
library comes with a custom resource that enables you to reference the AGA
security group.

Call `endpointGroup.connectionsPeer()` to obtain a reference to the Security Group
which you can use in connection rules. You must pass a reference to the VPC in whose
context the security group will be looked up. Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# ...

# Non-open ALB
alb = elbv2.ApplicationLoadBalancer(stack, "ALB")

endpoint_group = listener.add_endpoint_group("Group",
    endpoints=[
        ga_endpoints.ApplicationLoadBalancerEndpoint(alb,
            preserve_client_ips=True
        )
    ]
)

# Remember that there is only one AGA security group per VPC.
aga_sg = endpoint_group.connections_peer("GlobalAcceleratorSG", vpc)

# Allow connections from the AGA to the ALB
alb.connections.allow_from(aga_sg, Port.tcp(443))
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.core
import constructs


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.AcceleratorAttributes",
    jsii_struct_bases=[],
    name_mapping={"accelerator_arn": "acceleratorArn", "dns_name": "dnsName"},
)
class AcceleratorAttributes:
    def __init__(
        self,
        *,
        accelerator_arn: builtins.str,
        dns_name: builtins.str,
    ) -> None:
        '''Attributes required to import an existing accelerator to the stack.

        :param accelerator_arn: The ARN of the accelerator.
        :param dns_name: The DNS name of the accelerator.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator_arn": accelerator_arn,
            "dns_name": dns_name,
        }

    @builtins.property
    def accelerator_arn(self) -> builtins.str:
        '''The ARN of the accelerator.'''
        result = self._values.get("accelerator_arn")
        assert result is not None, "Required property 'accelerator_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dns_name(self) -> builtins.str:
        '''The DNS name of the accelerator.'''
        result = self._values.get("dns_name")
        assert result is not None, "Required property 'dns_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcceleratorAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.AcceleratorProps",
    jsii_struct_bases=[],
    name_mapping={"accelerator_name": "acceleratorName", "enabled": "enabled"},
)
class AcceleratorProps:
    def __init__(
        self,
        *,
        accelerator_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Construct properties of the Accelerator.

        :param accelerator_name: The name of the accelerator. Default: - resource ID
        :param enabled: Indicates whether the accelerator is enabled. Default: true
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if accelerator_name is not None:
            self._values["accelerator_name"] = accelerator_name
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def accelerator_name(self) -> typing.Optional[builtins.str]:
        '''The name of the accelerator.

        :default: - resource ID
        '''
        result = self._values.get("accelerator_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the accelerator is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcceleratorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAccelerator(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnAccelerator",
):
    '''A CloudFormation ``AWS::GlobalAccelerator::Accelerator``.

    :cloudformationResource: AWS::GlobalAccelerator::Accelerator
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::GlobalAccelerator::Accelerator``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::GlobalAccelerator::Accelerator.Name``.
        :param enabled: ``AWS::GlobalAccelerator::Accelerator.Enabled``.
        :param ip_addresses: ``AWS::GlobalAccelerator::Accelerator.IpAddresses``.
        :param ip_address_type: ``AWS::GlobalAccelerator::Accelerator.IpAddressType``.
        :param tags: ``AWS::GlobalAccelerator::Accelerator.Tags``.
        '''
        props = CfnAcceleratorProps(
            name=name,
            enabled=enabled,
            ip_addresses=ip_addresses,
            ip_address_type=ip_address_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrAcceleratorArn")
    def attr_accelerator_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: AcceleratorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAcceleratorArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDnsName")
    def attr_dns_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: DnsName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::GlobalAccelerator::Accelerator.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Accelerator.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabled")
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''``AWS::GlobalAccelerator::Accelerator.Enabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-enabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::GlobalAccelerator::Accelerator.IpAddresses``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresses
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "ipAddresses", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ipAddressType")
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::Accelerator.IpAddressType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresstype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressType"))

    @ip_address_type.setter
    def ip_address_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "ipAddressType", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnAcceleratorProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "enabled": "enabled",
        "ip_addresses": "ipAddresses",
        "ip_address_type": "ipAddressType",
        "tags": "tags",
    },
)
class CfnAcceleratorProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ip_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::GlobalAccelerator::Accelerator``.

        :param name: ``AWS::GlobalAccelerator::Accelerator.Name``.
        :param enabled: ``AWS::GlobalAccelerator::Accelerator.Enabled``.
        :param ip_addresses: ``AWS::GlobalAccelerator::Accelerator.IpAddresses``.
        :param ip_address_type: ``AWS::GlobalAccelerator::Accelerator.IpAddressType``.
        :param tags: ``AWS::GlobalAccelerator::Accelerator.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if ip_addresses is not None:
            self._values["ip_addresses"] = ip_addresses
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Accelerator.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
        '''``AWS::GlobalAccelerator::Accelerator.Enabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def ip_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::GlobalAccelerator::Accelerator.IpAddresses``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresses
        '''
        result = self._values.get("ip_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::Accelerator.IpAddressType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::GlobalAccelerator::Accelerator.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-accelerator.html#cfn-globalaccelerator-accelerator-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAcceleratorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEndpointGroup(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroup",
):
    '''A CloudFormation ``AWS::GlobalAccelerator::EndpointGroup``.

    :cloudformationResource: AWS::GlobalAccelerator::EndpointGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        endpoint_group_region: builtins.str,
        listener_arn: builtins.str,
        endpoint_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.EndpointConfigurationProperty"]]]] = None,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[jsii.Number] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        port_overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.PortOverrideProperty"]]]] = None,
        threshold_count: typing.Optional[jsii.Number] = None,
        traffic_dial_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::GlobalAccelerator::EndpointGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param endpoint_group_region: ``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.
        :param listener_arn: ``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.
        :param endpoint_configurations: ``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.
        :param health_check_interval_seconds: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.
        :param port_overrides: ``AWS::GlobalAccelerator::EndpointGroup.PortOverrides``.
        :param threshold_count: ``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.
        :param traffic_dial_percentage: ``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.
        '''
        props = CfnEndpointGroupProps(
            endpoint_group_region=endpoint_group_region,
            listener_arn=listener_arn,
            endpoint_configurations=endpoint_configurations,
            health_check_interval_seconds=health_check_interval_seconds,
            health_check_path=health_check_path,
            health_check_port=health_check_port,
            health_check_protocol=health_check_protocol,
            port_overrides=port_overrides,
            threshold_count=threshold_count,
            traffic_dial_percentage=traffic_dial_percentage,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrEndpointGroupArn")
    def attr_endpoint_group_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: EndpointGroupArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpointGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointGroupRegion")
    def endpoint_group_region(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointgroupregion
        '''
        return typing.cast(builtins.str, jsii.get(self, "endpointGroupRegion"))

    @endpoint_group_region.setter
    def endpoint_group_region(self, value: builtins.str) -> None:
        jsii.set(self, "endpointGroupRegion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-listenerarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

    @listener_arn.setter
    def listener_arn(self, value: builtins.str) -> None:
        jsii.set(self, "listenerArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointConfigurations")
    def endpoint_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.EndpointConfigurationProperty"]]]]:
        '''``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.EndpointConfigurationProperty"]]]], jsii.get(self, "endpointConfigurations"))

    @endpoint_configurations.setter
    def endpoint_configurations(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.EndpointConfigurationProperty"]]]],
    ) -> None:
        jsii.set(self, "endpointConfigurations", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckIntervalSeconds")
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckintervalseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthCheckIntervalSeconds"))

    @health_check_interval_seconds.setter
    def health_check_interval_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        jsii.set(self, "healthCheckIntervalSeconds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckpath
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckPath"))

    @health_check_path.setter
    def health_check_path(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckPath", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckPort")
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckport
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthCheckPort"))

    @health_check_port.setter
    def health_check_port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "healthCheckPort", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="healthCheckProtocol")
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckprotocol
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckProtocol"))

    @health_check_protocol.setter
    def health_check_protocol(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "healthCheckProtocol", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="portOverrides")
    def port_overrides(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.PortOverrideProperty"]]]]:
        '''``AWS::GlobalAccelerator::EndpointGroup.PortOverrides``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-portoverrides
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.PortOverrideProperty"]]]], jsii.get(self, "portOverrides"))

    @port_overrides.setter
    def port_overrides(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointGroup.PortOverrideProperty"]]]],
    ) -> None:
        jsii.set(self, "portOverrides", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="thresholdCount")
    def threshold_count(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-thresholdcount
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdCount"))

    @threshold_count.setter
    def threshold_count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "thresholdCount", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="trafficDialPercentage")
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-trafficdialpercentage
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "trafficDialPercentage"))

    @traffic_dial_percentage.setter
    def traffic_dial_percentage(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "trafficDialPercentage", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroup.EndpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint_id": "endpointId",
            "client_ip_preservation_enabled": "clientIpPreservationEnabled",
            "weight": "weight",
        },
    )
    class EndpointConfigurationProperty:
        def __init__(
            self,
            *,
            endpoint_id: builtins.str,
            client_ip_preservation_enabled: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param endpoint_id: ``CfnEndpointGroup.EndpointConfigurationProperty.EndpointId``.
            :param client_ip_preservation_enabled: ``CfnEndpointGroup.EndpointConfigurationProperty.ClientIPPreservationEnabled``.
            :param weight: ``CfnEndpointGroup.EndpointConfigurationProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "endpoint_id": endpoint_id,
            }
            if client_ip_preservation_enabled is not None:
                self._values["client_ip_preservation_enabled"] = client_ip_preservation_enabled
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def endpoint_id(self) -> builtins.str:
            '''``CfnEndpointGroup.EndpointConfigurationProperty.EndpointId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-endpointid
            '''
            result = self._values.get("endpoint_id")
            assert result is not None, "Required property 'endpoint_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_ip_preservation_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnEndpointGroup.EndpointConfigurationProperty.ClientIPPreservationEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-clientippreservationenabled
            '''
            result = self._values.get("client_ip_preservation_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''``CfnEndpointGroup.EndpointConfigurationProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-endpointconfiguration.html#cfn-globalaccelerator-endpointgroup-endpointconfiguration-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroup.PortOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint_port": "endpointPort",
            "listener_port": "listenerPort",
        },
    )
    class PortOverrideProperty:
        def __init__(
            self,
            *,
            endpoint_port: jsii.Number,
            listener_port: jsii.Number,
        ) -> None:
            '''
            :param endpoint_port: ``CfnEndpointGroup.PortOverrideProperty.EndpointPort``.
            :param listener_port: ``CfnEndpointGroup.PortOverrideProperty.ListenerPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-portoverride.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "endpoint_port": endpoint_port,
                "listener_port": listener_port,
            }

        @builtins.property
        def endpoint_port(self) -> jsii.Number:
            '''``CfnEndpointGroup.PortOverrideProperty.EndpointPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-portoverride.html#cfn-globalaccelerator-endpointgroup-portoverride-endpointport
            '''
            result = self._values.get("endpoint_port")
            assert result is not None, "Required property 'endpoint_port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def listener_port(self) -> jsii.Number:
            '''``CfnEndpointGroup.PortOverrideProperty.ListenerPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-endpointgroup-portoverride.html#cfn-globalaccelerator-endpointgroup-portoverride-listenerport
            '''
            result = self._values.get("listener_port")
            assert result is not None, "Required property 'listener_port' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnEndpointGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_group_region": "endpointGroupRegion",
        "listener_arn": "listenerArn",
        "endpoint_configurations": "endpointConfigurations",
        "health_check_interval_seconds": "healthCheckIntervalSeconds",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "port_overrides": "portOverrides",
        "threshold_count": "thresholdCount",
        "traffic_dial_percentage": "trafficDialPercentage",
    },
)
class CfnEndpointGroupProps:
    def __init__(
        self,
        *,
        endpoint_group_region: builtins.str,
        listener_arn: builtins.str,
        endpoint_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.EndpointConfigurationProperty]]]] = None,
        health_check_interval_seconds: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[jsii.Number] = None,
        health_check_protocol: typing.Optional[builtins.str] = None,
        port_overrides: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.PortOverrideProperty]]]] = None,
        threshold_count: typing.Optional[jsii.Number] = None,
        traffic_dial_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``AWS::GlobalAccelerator::EndpointGroup``.

        :param endpoint_group_region: ``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.
        :param listener_arn: ``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.
        :param endpoint_configurations: ``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.
        :param health_check_interval_seconds: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.
        :param health_check_path: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.
        :param health_check_port: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.
        :param health_check_protocol: ``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.
        :param port_overrides: ``AWS::GlobalAccelerator::EndpointGroup.PortOverrides``.
        :param threshold_count: ``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.
        :param traffic_dial_percentage: ``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_group_region": endpoint_group_region,
            "listener_arn": listener_arn,
        }
        if endpoint_configurations is not None:
            self._values["endpoint_configurations"] = endpoint_configurations
        if health_check_interval_seconds is not None:
            self._values["health_check_interval_seconds"] = health_check_interval_seconds
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if port_overrides is not None:
            self._values["port_overrides"] = port_overrides
        if threshold_count is not None:
            self._values["threshold_count"] = threshold_count
        if traffic_dial_percentage is not None:
            self._values["traffic_dial_percentage"] = traffic_dial_percentage

    @builtins.property
    def endpoint_group_region(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::EndpointGroup.EndpointGroupRegion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointgroupregion
        '''
        result = self._values.get("endpoint_group_region")
        assert result is not None, "Required property 'endpoint_group_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def listener_arn(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::EndpointGroup.ListenerArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-listenerarn
        '''
        result = self._values.get("listener_arn")
        assert result is not None, "Required property 'listener_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_configurations(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.EndpointConfigurationProperty]]]]:
        '''``AWS::GlobalAccelerator::EndpointGroup.EndpointConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-endpointconfigurations
        '''
        result = self._values.get("endpoint_configurations")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.EndpointConfigurationProperty]]]], result)

    @builtins.property
    def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckIntervalSeconds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckintervalseconds
        '''
        result = self._values.get("health_check_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPath``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckpath
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckPort``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckport
        '''
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_protocol(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::EndpointGroup.HealthCheckProtocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-healthcheckprotocol
        '''
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_overrides(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.PortOverrideProperty]]]]:
        '''``AWS::GlobalAccelerator::EndpointGroup.PortOverrides``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-portoverrides
        '''
        result = self._values.get("port_overrides")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnEndpointGroup.PortOverrideProperty]]]], result)

    @builtins.property
    def threshold_count(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.ThresholdCount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-thresholdcount
        '''
        result = self._values.get("threshold_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        '''``AWS::GlobalAccelerator::EndpointGroup.TrafficDialPercentage``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-endpointgroup.html#cfn-globalaccelerator-endpointgroup-trafficdialpercentage
        '''
        result = self._values.get("traffic_dial_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEndpointGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnListener(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnListener",
):
    '''A CloudFormation ``AWS::GlobalAccelerator::Listener``.

    :cloudformationResource: AWS::GlobalAccelerator::Listener
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        accelerator_arn: builtins.str,
        port_ranges: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnListener.PortRangeProperty"]]],
        protocol: builtins.str,
        client_affinity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::GlobalAccelerator::Listener``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param accelerator_arn: ``AWS::GlobalAccelerator::Listener.AcceleratorArn``.
        :param port_ranges: ``AWS::GlobalAccelerator::Listener.PortRanges``.
        :param protocol: ``AWS::GlobalAccelerator::Listener.Protocol``.
        :param client_affinity: ``AWS::GlobalAccelerator::Listener.ClientAffinity``.
        '''
        props = CfnListenerProps(
            accelerator_arn=accelerator_arn,
            port_ranges=port_ranges,
            protocol=protocol,
            client_affinity=client_affinity,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrListenerArn")
    def attr_listener_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ListenerArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrListenerArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Listener.AcceleratorArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-acceleratorarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "acceleratorArn"))

    @accelerator_arn.setter
    def accelerator_arn(self, value: builtins.str) -> None:
        jsii.set(self, "acceleratorArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="portRanges")
    def port_ranges(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.PortRangeProperty"]]]:
        '''``AWS::GlobalAccelerator::Listener.PortRanges``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-portranges
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.PortRangeProperty"]]], jsii.get(self, "portRanges"))

    @port_ranges.setter
    def port_ranges(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnListener.PortRangeProperty"]]],
    ) -> None:
        jsii.set(self, "portRanges", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Listener.Protocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-protocol
        '''
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        jsii.set(self, "protocol", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clientAffinity")
    def client_affinity(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-clientaffinity
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientAffinity"))

    @client_affinity.setter
    def client_affinity(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clientAffinity", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-globalaccelerator.CfnListener.PortRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"from_port": "fromPort", "to_port": "toPort"},
    )
    class PortRangeProperty:
        def __init__(self, *, from_port: jsii.Number, to_port: jsii.Number) -> None:
            '''
            :param from_port: ``CfnListener.PortRangeProperty.FromPort``.
            :param to_port: ``CfnListener.PortRangeProperty.ToPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "from_port": from_port,
                "to_port": to_port,
            }

        @builtins.property
        def from_port(self) -> jsii.Number:
            '''``CfnListener.PortRangeProperty.FromPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html#cfn-globalaccelerator-listener-portrange-fromport
            '''
            result = self._values.get("from_port")
            assert result is not None, "Required property 'from_port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def to_port(self) -> jsii.Number:
            '''``CfnListener.PortRangeProperty.ToPort``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-globalaccelerator-listener-portrange.html#cfn-globalaccelerator-listener-portrange-toport
            '''
            result = self._values.get("to_port")
            assert result is not None, "Required property 'to_port' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.CfnListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_arn": "acceleratorArn",
        "port_ranges": "portRanges",
        "protocol": "protocol",
        "client_affinity": "clientAffinity",
    },
)
class CfnListenerProps:
    def __init__(
        self,
        *,
        accelerator_arn: builtins.str,
        port_ranges: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, CfnListener.PortRangeProperty]]],
        protocol: builtins.str,
        client_affinity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::GlobalAccelerator::Listener``.

        :param accelerator_arn: ``AWS::GlobalAccelerator::Listener.AcceleratorArn``.
        :param port_ranges: ``AWS::GlobalAccelerator::Listener.PortRanges``.
        :param protocol: ``AWS::GlobalAccelerator::Listener.Protocol``.
        :param client_affinity: ``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "accelerator_arn": accelerator_arn,
            "port_ranges": port_ranges,
            "protocol": protocol,
        }
        if client_affinity is not None:
            self._values["client_affinity"] = client_affinity

    @builtins.property
    def accelerator_arn(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Listener.AcceleratorArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-acceleratorarn
        '''
        result = self._values.get("accelerator_arn")
        assert result is not None, "Required property 'accelerator_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port_ranges(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListener.PortRangeProperty]]]:
        '''``AWS::GlobalAccelerator::Listener.PortRanges``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-portranges
        '''
        result = self._values.get("port_ranges")
        assert result is not None, "Required property 'port_ranges' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnListener.PortRangeProperty]]], result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''``AWS::GlobalAccelerator::Listener.Protocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-protocol
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_affinity(self) -> typing.Optional[builtins.str]:
        '''``AWS::GlobalAccelerator::Listener.ClientAffinity``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-globalaccelerator-listener.html#cfn-globalaccelerator-listener-clientaffinity
        '''
        result = self._values.get("client_affinity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-globalaccelerator.ClientAffinity")
class ClientAffinity(enum.Enum):
    '''Client affinity gives you control over whether to always route each client to the same specific endpoint.

    :see: https://docs.aws.amazon.com/global-accelerator/latest/dg/about-listeners.html#about-listeners-client-affinity
    '''

    NONE = "NONE"
    '''Route traffic based on the 5-tuple ``(source IP, source port, destination IP, destination port, protocol)``.'''
    SOURCE_IP = "SOURCE_IP"
    '''Route traffic based on the 2-tuple ``(source IP, destination IP)``.

    The result is that multiple connections from the same client will be routed the same.
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-globalaccelerator.ConnectionProtocol")
class ConnectionProtocol(enum.Enum):
    '''The protocol for the connections from clients to the accelerator.'''

    TCP = "TCP"
    '''TCP.'''
    UDP = "UDP"
    '''UDP.'''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.EndpointGroupOptions",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_group_name": "endpointGroupName",
        "endpoints": "endpoints",
        "health_check_interval": "healthCheckInterval",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "health_check_threshold": "healthCheckThreshold",
        "port_overrides": "portOverrides",
        "region": "region",
        "traffic_dial_percentage": "trafficDialPercentage",
    },
)
class EndpointGroupOptions:
    def __init__(
        self,
        *,
        endpoint_group_name: typing.Optional[builtins.str] = None,
        endpoints: typing.Optional[typing.Sequence["IEndpoint"]] = None,
        health_check_interval: typing.Optional[aws_cdk.core.Duration] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[jsii.Number] = None,
        health_check_protocol: typing.Optional["HealthCheckProtocol"] = None,
        health_check_threshold: typing.Optional[jsii.Number] = None,
        port_overrides: typing.Optional[typing.Sequence["PortOverride"]] = None,
        region: typing.Optional[builtins.str] = None,
        traffic_dial_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Basic options for creating a new EndpointGroup.

        :param endpoint_group_name: Name of the endpoint group. Default: - logical ID of the resource
        :param endpoints: Initial list of endpoints for this group. Default: - Group is initially empty
        :param health_check_interval: The time between health checks for each endpoint. Must be either 10 or 30 seconds. Default: Duration.seconds(30)
        :param health_check_path: The ping path for health checks (if the protocol is HTTP(S)). Default: '/'
        :param health_check_port: The port used to perform health checks. Default: - The listener's port
        :param health_check_protocol: The protocol used to perform health checks. Default: HealthCheckProtocol.TCP
        :param health_check_threshold: The number of consecutive health checks required to set the state of a healthy endpoint to unhealthy, or to set an unhealthy endpoint to healthy. Default: 3
        :param port_overrides: Override the destination ports used to route traffic to an endpoint. Unless overridden, the port used to hit the endpoint will be the same as the port that traffic arrives on at the listener. Default: - No overrides
        :param region: The AWS Region where the endpoint group is located. Default: - region of the first endpoint in this group, or the stack region if that region can't be determined
        :param traffic_dial_percentage: The percentage of traffic to send to this AWS Region. The percentage is applied to the traffic that would otherwise have been routed to the Region based on optimal routing. Additional traffic is distributed to other endpoint groups for this listener. Default: 100
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if endpoint_group_name is not None:
            self._values["endpoint_group_name"] = endpoint_group_name
        if endpoints is not None:
            self._values["endpoints"] = endpoints
        if health_check_interval is not None:
            self._values["health_check_interval"] = health_check_interval
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if health_check_threshold is not None:
            self._values["health_check_threshold"] = health_check_threshold
        if port_overrides is not None:
            self._values["port_overrides"] = port_overrides
        if region is not None:
            self._values["region"] = region
        if traffic_dial_percentage is not None:
            self._values["traffic_dial_percentage"] = traffic_dial_percentage

    @builtins.property
    def endpoint_group_name(self) -> typing.Optional[builtins.str]:
        '''Name of the endpoint group.

        :default: - logical ID of the resource
        '''
        result = self._values.get("endpoint_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoints(self) -> typing.Optional[typing.List["IEndpoint"]]:
        '''Initial list of endpoints for this group.

        :default: - Group is initially empty
        '''
        result = self._values.get("endpoints")
        return typing.cast(typing.Optional[typing.List["IEndpoint"]], result)

    @builtins.property
    def health_check_interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''The time between health checks for each endpoint.

        Must be either 10 or 30 seconds.

        :default: Duration.seconds(30)
        '''
        result = self._values.get("health_check_interval")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''The ping path for health checks (if the protocol is HTTP(S)).

        :default: '/'
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        '''The port used to perform health checks.

        :default: - The listener's port
        '''
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_protocol(self) -> typing.Optional["HealthCheckProtocol"]:
        '''The protocol used to perform health checks.

        :default: HealthCheckProtocol.TCP
        '''
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional["HealthCheckProtocol"], result)

    @builtins.property
    def health_check_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive health checks required to set the state of a healthy endpoint to unhealthy, or to set an unhealthy endpoint to healthy.

        :default: 3
        '''
        result = self._values.get("health_check_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_overrides(self) -> typing.Optional[typing.List["PortOverride"]]:
        '''Override the destination ports used to route traffic to an endpoint.

        Unless overridden, the port used to hit the endpoint will be the same as the port
        that traffic arrives on at the listener.

        :default: - No overrides
        '''
        result = self._values.get("port_overrides")
        return typing.cast(typing.Optional[typing.List["PortOverride"]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS Region where the endpoint group is located.

        :default: - region of the first endpoint in this group, or the stack region if that region can't be determined
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of traffic to send to this AWS Region.

        The percentage is applied to the traffic that would otherwise have been
        routed to the Region based on optimal routing. Additional traffic is
        distributed to other endpoint groups for this listener.

        :default: 100
        '''
        result = self._values.get("traffic_dial_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointGroupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.EndpointGroupProps",
    jsii_struct_bases=[EndpointGroupOptions],
    name_mapping={
        "endpoint_group_name": "endpointGroupName",
        "endpoints": "endpoints",
        "health_check_interval": "healthCheckInterval",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "health_check_threshold": "healthCheckThreshold",
        "port_overrides": "portOverrides",
        "region": "region",
        "traffic_dial_percentage": "trafficDialPercentage",
        "listener": "listener",
    },
)
class EndpointGroupProps(EndpointGroupOptions):
    def __init__(
        self,
        *,
        endpoint_group_name: typing.Optional[builtins.str] = None,
        endpoints: typing.Optional[typing.Sequence["IEndpoint"]] = None,
        health_check_interval: typing.Optional[aws_cdk.core.Duration] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[jsii.Number] = None,
        health_check_protocol: typing.Optional["HealthCheckProtocol"] = None,
        health_check_threshold: typing.Optional[jsii.Number] = None,
        port_overrides: typing.Optional[typing.Sequence["PortOverride"]] = None,
        region: typing.Optional[builtins.str] = None,
        traffic_dial_percentage: typing.Optional[jsii.Number] = None,
        listener: "IListener",
    ) -> None:
        '''Property of the EndpointGroup.

        :param endpoint_group_name: Name of the endpoint group. Default: - logical ID of the resource
        :param endpoints: Initial list of endpoints for this group. Default: - Group is initially empty
        :param health_check_interval: The time between health checks for each endpoint. Must be either 10 or 30 seconds. Default: Duration.seconds(30)
        :param health_check_path: The ping path for health checks (if the protocol is HTTP(S)). Default: '/'
        :param health_check_port: The port used to perform health checks. Default: - The listener's port
        :param health_check_protocol: The protocol used to perform health checks. Default: HealthCheckProtocol.TCP
        :param health_check_threshold: The number of consecutive health checks required to set the state of a healthy endpoint to unhealthy, or to set an unhealthy endpoint to healthy. Default: 3
        :param port_overrides: Override the destination ports used to route traffic to an endpoint. Unless overridden, the port used to hit the endpoint will be the same as the port that traffic arrives on at the listener. Default: - No overrides
        :param region: The AWS Region where the endpoint group is located. Default: - region of the first endpoint in this group, or the stack region if that region can't be determined
        :param traffic_dial_percentage: The percentage of traffic to send to this AWS Region. The percentage is applied to the traffic that would otherwise have been routed to the Region based on optimal routing. Additional traffic is distributed to other endpoint groups for this listener. Default: 100
        :param listener: The Amazon Resource Name (ARN) of the listener.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }
        if endpoint_group_name is not None:
            self._values["endpoint_group_name"] = endpoint_group_name
        if endpoints is not None:
            self._values["endpoints"] = endpoints
        if health_check_interval is not None:
            self._values["health_check_interval"] = health_check_interval
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if health_check_threshold is not None:
            self._values["health_check_threshold"] = health_check_threshold
        if port_overrides is not None:
            self._values["port_overrides"] = port_overrides
        if region is not None:
            self._values["region"] = region
        if traffic_dial_percentage is not None:
            self._values["traffic_dial_percentage"] = traffic_dial_percentage

    @builtins.property
    def endpoint_group_name(self) -> typing.Optional[builtins.str]:
        '''Name of the endpoint group.

        :default: - logical ID of the resource
        '''
        result = self._values.get("endpoint_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoints(self) -> typing.Optional[typing.List["IEndpoint"]]:
        '''Initial list of endpoints for this group.

        :default: - Group is initially empty
        '''
        result = self._values.get("endpoints")
        return typing.cast(typing.Optional[typing.List["IEndpoint"]], result)

    @builtins.property
    def health_check_interval(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''The time between health checks for each endpoint.

        Must be either 10 or 30 seconds.

        :default: Duration.seconds(30)
        '''
        result = self._values.get("health_check_interval")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''The ping path for health checks (if the protocol is HTTP(S)).

        :default: '/'
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        '''The port used to perform health checks.

        :default: - The listener's port
        '''
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_protocol(self) -> typing.Optional["HealthCheckProtocol"]:
        '''The protocol used to perform health checks.

        :default: HealthCheckProtocol.TCP
        '''
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional["HealthCheckProtocol"], result)

    @builtins.property
    def health_check_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive health checks required to set the state of a healthy endpoint to unhealthy, or to set an unhealthy endpoint to healthy.

        :default: 3
        '''
        result = self._values.get("health_check_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_overrides(self) -> typing.Optional[typing.List["PortOverride"]]:
        '''Override the destination ports used to route traffic to an endpoint.

        Unless overridden, the port used to hit the endpoint will be the same as the port
        that traffic arrives on at the listener.

        :default: - No overrides
        '''
        result = self._values.get("port_overrides")
        return typing.cast(typing.Optional[typing.List["PortOverride"]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS Region where the endpoint group is located.

        :default: - region of the first endpoint in this group, or the stack region if that region can't be determined
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def traffic_dial_percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of traffic to send to this AWS Region.

        The percentage is applied to the traffic that would otherwise have been
        routed to the Region based on optimal routing. Additional traffic is
        distributed to other endpoint groups for this listener.

        :default: 100
        '''
        result = self._values.get("traffic_dial_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def listener(self) -> "IListener":
        '''The Amazon Resource Name (ARN) of the listener.'''
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return typing.cast("IListener", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-globalaccelerator.HealthCheckProtocol")
class HealthCheckProtocol(enum.Enum):
    '''The protocol for the connections from clients to the accelerator.'''

    TCP = "TCP"
    '''TCP.'''
    HTTP = "HTTP"
    '''HTTP.'''
    HTTPS = "HTTPS"
    '''HTTPS.'''


@jsii.interface(jsii_type="@aws-cdk/aws-globalaccelerator.IAccelerator")
class IAccelerator(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''The interface of the Accelerator.'''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> builtins.str:
        '''The ARN of the accelerator.

        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        '''The Domain Name System (DNS) name that Global Accelerator creates that points to your accelerator's static IP addresses.

        :attribute: true
        '''
        ...


class _IAcceleratorProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''The interface of the Accelerator.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-globalaccelerator.IAccelerator"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> builtins.str:
        '''The ARN of the accelerator.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "acceleratorArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        '''The Domain Name System (DNS) name that Global Accelerator creates that points to your accelerator's static IP addresses.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAccelerator).__jsii_proxy_class__ = lambda : _IAcceleratorProxy


@jsii.interface(jsii_type="@aws-cdk/aws-globalaccelerator.IEndpoint")
class IEndpoint(typing_extensions.Protocol):
    '''An endpoint for the endpoint group.

    Implementations of ``IEndpoint`` can be found in the ``aws-globalaccelerator-endpoints`` package.
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''The region where the endpoint is located.

        If the region cannot be determined, ``undefined`` is returned
        '''
        ...

    @jsii.member(jsii_name="renderEndpointConfiguration")
    def render_endpoint_configuration(self) -> typing.Any:
        '''Render the endpoint to an endpoint configuration.'''
        ...


class _IEndpointProxy:
    '''An endpoint for the endpoint group.

    Implementations of ``IEndpoint`` can be found in the ``aws-globalaccelerator-endpoints`` package.
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-globalaccelerator.IEndpoint"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''The region where the endpoint is located.

        If the region cannot be determined, ``undefined`` is returned
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @jsii.member(jsii_name="renderEndpointConfiguration")
    def render_endpoint_configuration(self) -> typing.Any:
        '''Render the endpoint to an endpoint configuration.'''
        return typing.cast(typing.Any, jsii.invoke(self, "renderEndpointConfiguration", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEndpoint).__jsii_proxy_class__ = lambda : _IEndpointProxy


@jsii.interface(jsii_type="@aws-cdk/aws-globalaccelerator.IEndpointGroup")
class IEndpointGroup(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''The interface of the EndpointGroup.'''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointGroupArn")
    def endpoint_group_arn(self) -> builtins.str:
        '''EndpointGroup ARN.

        :attribute: true
        '''
        ...


class _IEndpointGroupProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''The interface of the EndpointGroup.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-globalaccelerator.IEndpointGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointGroupArn")
    def endpoint_group_arn(self) -> builtins.str:
        '''EndpointGroup ARN.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "endpointGroupArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEndpointGroup).__jsii_proxy_class__ = lambda : _IEndpointGroupProxy


@jsii.interface(jsii_type="@aws-cdk/aws-globalaccelerator.IListener")
class IListener(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''Interface of the Listener.'''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''The ARN of the listener.

        :attribute: true
        '''
        ...


class _IListenerProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''Interface of the Listener.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-globalaccelerator.IListener"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''The ARN of the listener.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IListener).__jsii_proxy_class__ = lambda : _IListenerProxy


@jsii.implements(IListener)
class Listener(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.Listener",
):
    '''The construct for the Listener.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        accelerator: IAccelerator,
        port_ranges: typing.Sequence["PortRange"],
        client_affinity: typing.Optional[ClientAffinity] = None,
        listener_name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[ConnectionProtocol] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param accelerator: The accelerator for this listener.
        :param port_ranges: The list of port ranges for the connections from clients to the accelerator.
        :param client_affinity: Client affinity to direct all requests from a user to the same endpoint. If you have stateful applications, client affinity lets you direct all requests from a user to the same endpoint. By default, each connection from each client is routed to seperate endpoints. Set client affinity to SOURCE_IP to route all connections from a single client to the same endpoint. Default: ClientAffinity.NONE
        :param listener_name: Name of the listener. Default: - logical ID of the resource
        :param protocol: The protocol for the connections from clients to the accelerator. Default: ConnectionProtocol.TCP
        '''
        props = ListenerProps(
            accelerator=accelerator,
            port_ranges=port_ranges,
            client_affinity=client_affinity,
            listener_name=listener_name,
            protocol=protocol,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromListenerArn") # type: ignore[misc]
    @builtins.classmethod
    def from_listener_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        listener_arn: builtins.str,
    ) -> IListener:
        '''import from ARN.

        :param scope: -
        :param id: -
        :param listener_arn: -
        '''
        return typing.cast(IListener, jsii.sinvoke(cls, "fromListenerArn", [scope, id, listener_arn]))

    @jsii.member(jsii_name="addEndpointGroup")
    def add_endpoint_group(
        self,
        id: builtins.str,
        *,
        endpoint_group_name: typing.Optional[builtins.str] = None,
        endpoints: typing.Optional[typing.Sequence[IEndpoint]] = None,
        health_check_interval: typing.Optional[aws_cdk.core.Duration] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[jsii.Number] = None,
        health_check_protocol: typing.Optional[HealthCheckProtocol] = None,
        health_check_threshold: typing.Optional[jsii.Number] = None,
        port_overrides: typing.Optional[typing.Sequence["PortOverride"]] = None,
        region: typing.Optional[builtins.str] = None,
        traffic_dial_percentage: typing.Optional[jsii.Number] = None,
    ) -> "EndpointGroup":
        '''Add a new endpoint group to this listener.

        :param id: -
        :param endpoint_group_name: Name of the endpoint group. Default: - logical ID of the resource
        :param endpoints: Initial list of endpoints for this group. Default: - Group is initially empty
        :param health_check_interval: The time between health checks for each endpoint. Must be either 10 or 30 seconds. Default: Duration.seconds(30)
        :param health_check_path: The ping path for health checks (if the protocol is HTTP(S)). Default: '/'
        :param health_check_port: The port used to perform health checks. Default: - The listener's port
        :param health_check_protocol: The protocol used to perform health checks. Default: HealthCheckProtocol.TCP
        :param health_check_threshold: The number of consecutive health checks required to set the state of a healthy endpoint to unhealthy, or to set an unhealthy endpoint to healthy. Default: 3
        :param port_overrides: Override the destination ports used to route traffic to an endpoint. Unless overridden, the port used to hit the endpoint will be the same as the port that traffic arrives on at the listener. Default: - No overrides
        :param region: The AWS Region where the endpoint group is located. Default: - region of the first endpoint in this group, or the stack region if that region can't be determined
        :param traffic_dial_percentage: The percentage of traffic to send to this AWS Region. The percentage is applied to the traffic that would otherwise have been routed to the Region based on optimal routing. Additional traffic is distributed to other endpoint groups for this listener. Default: 100
        '''
        options = EndpointGroupOptions(
            endpoint_group_name=endpoint_group_name,
            endpoints=endpoints,
            health_check_interval=health_check_interval,
            health_check_path=health_check_path,
            health_check_port=health_check_port,
            health_check_protocol=health_check_protocol,
            health_check_threshold=health_check_threshold,
            port_overrides=port_overrides,
            region=region,
            traffic_dial_percentage=traffic_dial_percentage,
        )

        return typing.cast("EndpointGroup", jsii.invoke(self, "addEndpointGroup", [id, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerArn")
    def listener_arn(self) -> builtins.str:
        '''The ARN of the listener.'''
        return typing.cast(builtins.str, jsii.get(self, "listenerArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="listenerName")
    def listener_name(self) -> builtins.str:
        '''The name of the listener.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "listenerName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.ListenerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "port_ranges": "portRanges",
        "client_affinity": "clientAffinity",
        "listener_name": "listenerName",
        "protocol": "protocol",
    },
)
class ListenerOptions:
    def __init__(
        self,
        *,
        port_ranges: typing.Sequence["PortRange"],
        client_affinity: typing.Optional[ClientAffinity] = None,
        listener_name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[ConnectionProtocol] = None,
    ) -> None:
        '''Construct options for Listener.

        :param port_ranges: The list of port ranges for the connections from clients to the accelerator.
        :param client_affinity: Client affinity to direct all requests from a user to the same endpoint. If you have stateful applications, client affinity lets you direct all requests from a user to the same endpoint. By default, each connection from each client is routed to seperate endpoints. Set client affinity to SOURCE_IP to route all connections from a single client to the same endpoint. Default: ClientAffinity.NONE
        :param listener_name: Name of the listener. Default: - logical ID of the resource
        :param protocol: The protocol for the connections from clients to the accelerator. Default: ConnectionProtocol.TCP
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "port_ranges": port_ranges,
        }
        if client_affinity is not None:
            self._values["client_affinity"] = client_affinity
        if listener_name is not None:
            self._values["listener_name"] = listener_name
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def port_ranges(self) -> typing.List["PortRange"]:
        '''The list of port ranges for the connections from clients to the accelerator.'''
        result = self._values.get("port_ranges")
        assert result is not None, "Required property 'port_ranges' is missing"
        return typing.cast(typing.List["PortRange"], result)

    @builtins.property
    def client_affinity(self) -> typing.Optional[ClientAffinity]:
        '''Client affinity to direct all requests from a user to the same endpoint.

        If you have stateful applications, client affinity lets you direct all
        requests from a user to the same endpoint.

        By default, each connection from each client is routed to seperate
        endpoints. Set client affinity to SOURCE_IP to route all connections from
        a single client to the same endpoint.

        :default: ClientAffinity.NONE
        '''
        result = self._values.get("client_affinity")
        return typing.cast(typing.Optional[ClientAffinity], result)

    @builtins.property
    def listener_name(self) -> typing.Optional[builtins.str]:
        '''Name of the listener.

        :default: - logical ID of the resource
        '''
        result = self._values.get("listener_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[ConnectionProtocol]:
        '''The protocol for the connections from clients to the accelerator.

        :default: ConnectionProtocol.TCP
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[ConnectionProtocol], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ListenerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.ListenerProps",
    jsii_struct_bases=[ListenerOptions],
    name_mapping={
        "port_ranges": "portRanges",
        "client_affinity": "clientAffinity",
        "listener_name": "listenerName",
        "protocol": "protocol",
        "accelerator": "accelerator",
    },
)
class ListenerProps(ListenerOptions):
    def __init__(
        self,
        *,
        port_ranges: typing.Sequence["PortRange"],
        client_affinity: typing.Optional[ClientAffinity] = None,
        listener_name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[ConnectionProtocol] = None,
        accelerator: IAccelerator,
    ) -> None:
        '''Construct properties for Listener.

        :param port_ranges: The list of port ranges for the connections from clients to the accelerator.
        :param client_affinity: Client affinity to direct all requests from a user to the same endpoint. If you have stateful applications, client affinity lets you direct all requests from a user to the same endpoint. By default, each connection from each client is routed to seperate endpoints. Set client affinity to SOURCE_IP to route all connections from a single client to the same endpoint. Default: ClientAffinity.NONE
        :param listener_name: Name of the listener. Default: - logical ID of the resource
        :param protocol: The protocol for the connections from clients to the accelerator. Default: ConnectionProtocol.TCP
        :param accelerator: The accelerator for this listener.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "port_ranges": port_ranges,
            "accelerator": accelerator,
        }
        if client_affinity is not None:
            self._values["client_affinity"] = client_affinity
        if listener_name is not None:
            self._values["listener_name"] = listener_name
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def port_ranges(self) -> typing.List["PortRange"]:
        '''The list of port ranges for the connections from clients to the accelerator.'''
        result = self._values.get("port_ranges")
        assert result is not None, "Required property 'port_ranges' is missing"
        return typing.cast(typing.List["PortRange"], result)

    @builtins.property
    def client_affinity(self) -> typing.Optional[ClientAffinity]:
        '''Client affinity to direct all requests from a user to the same endpoint.

        If you have stateful applications, client affinity lets you direct all
        requests from a user to the same endpoint.

        By default, each connection from each client is routed to seperate
        endpoints. Set client affinity to SOURCE_IP to route all connections from
        a single client to the same endpoint.

        :default: ClientAffinity.NONE
        '''
        result = self._values.get("client_affinity")
        return typing.cast(typing.Optional[ClientAffinity], result)

    @builtins.property
    def listener_name(self) -> typing.Optional[builtins.str]:
        '''Name of the listener.

        :default: - logical ID of the resource
        '''
        result = self._values.get("listener_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[ConnectionProtocol]:
        '''The protocol for the connections from clients to the accelerator.

        :default: ConnectionProtocol.TCP
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[ConnectionProtocol], result)

    @builtins.property
    def accelerator(self) -> IAccelerator:
        '''The accelerator for this listener.'''
        result = self._values.get("accelerator")
        assert result is not None, "Required property 'accelerator' is missing"
        return typing.cast(IAccelerator, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.PortOverride",
    jsii_struct_bases=[],
    name_mapping={"endpoint_port": "endpointPort", "listener_port": "listenerPort"},
)
class PortOverride:
    def __init__(
        self,
        *,
        endpoint_port: jsii.Number,
        listener_port: jsii.Number,
    ) -> None:
        '''Override specific listener ports used to route traffic to endpoints that are part of an endpoint group.

        :param endpoint_port: The endpoint port that you want a listener port to be mapped to. This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.
        :param listener_port: The listener port that you want to map to a specific endpoint port. This is the port that user traffic arrives to the Global Accelerator on.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_port": endpoint_port,
            "listener_port": listener_port,
        }

    @builtins.property
    def endpoint_port(self) -> jsii.Number:
        '''The endpoint port that you want a listener port to be mapped to.

        This is the port on the endpoint, such as the Application Load Balancer or Amazon EC2 instance.
        '''
        result = self._values.get("endpoint_port")
        assert result is not None, "Required property 'endpoint_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def listener_port(self) -> jsii.Number:
        '''The listener port that you want to map to a specific endpoint port.

        This is the port that user traffic arrives to the Global Accelerator on.
        '''
        result = self._values.get("listener_port")
        assert result is not None, "Required property 'listener_port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PortOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.PortRange",
    jsii_struct_bases=[],
    name_mapping={"from_port": "fromPort", "to_port": "toPort"},
)
class PortRange:
    def __init__(
        self,
        *,
        from_port: jsii.Number,
        to_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''The list of port ranges for the connections from clients to the accelerator.

        :param from_port: The first port in the range of ports, inclusive.
        :param to_port: The last port in the range of ports, inclusive. Default: - same as ``fromPort``
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "from_port": from_port,
        }
        if to_port is not None:
            self._values["to_port"] = to_port

    @builtins.property
    def from_port(self) -> jsii.Number:
        '''The first port in the range of ports, inclusive.'''
        result = self._values.get("from_port")
        assert result is not None, "Required property 'from_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def to_port(self) -> typing.Optional[jsii.Number]:
        '''The last port in the range of ports, inclusive.

        :default: - same as ``fromPort``
        '''
        result = self._values.get("to_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PortRange(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IEndpoint)
class RawEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.RawEndpoint",
):
    '''Untyped endpoint implementation.

    Prefer using the classes in the ``aws-globalaccelerator-endpoints`` package instead,
    as they accept typed constructs. You can use this class if you want to use an
    endpoint type that does not have an appropriate class in that package yet.
    '''

    def __init__(
        self,
        *,
        endpoint_id: builtins.str,
        preserve_client_ip: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param endpoint_id: Identifier of the endpoint. Load balancer ARN, instance ID or EIP allocation ID.
        :param preserve_client_ip: Forward the client IP address. GlobalAccelerator will create Network Interfaces in your VPC in order to preserve the client IP address. Only applies to Application Load Balancers and EC2 instances. Client IP address preservation is supported only in specific AWS Regions. See the GlobalAccelerator Developer Guide for a list. Default: true if possible and available
        :param region: The region where this endpoint is located. Default: - Unknown what region this endpoint is located
        :param weight: Endpoint weight across all endpoints in the group. Must be a value between 0 and 255. Default: 128
        '''
        props = RawEndpointProps(
            endpoint_id=endpoint_id,
            preserve_client_ip=preserve_client_ip,
            region=region,
            weight=weight,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="renderEndpointConfiguration")
    def render_endpoint_configuration(self) -> typing.Any:
        '''Render the endpoint to an endpoint configuration.'''
        return typing.cast(typing.Any, jsii.invoke(self, "renderEndpointConfiguration", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''The region where the endpoint is located.

        If the region cannot be determined, ``undefined`` is returned
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-globalaccelerator.RawEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_id": "endpointId",
        "preserve_client_ip": "preserveClientIp",
        "region": "region",
        "weight": "weight",
    },
)
class RawEndpointProps:
    def __init__(
        self,
        *,
        endpoint_id: builtins.str,
        preserve_client_ip: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for RawEndpoint.

        :param endpoint_id: Identifier of the endpoint. Load balancer ARN, instance ID or EIP allocation ID.
        :param preserve_client_ip: Forward the client IP address. GlobalAccelerator will create Network Interfaces in your VPC in order to preserve the client IP address. Only applies to Application Load Balancers and EC2 instances. Client IP address preservation is supported only in specific AWS Regions. See the GlobalAccelerator Developer Guide for a list. Default: true if possible and available
        :param region: The region where this endpoint is located. Default: - Unknown what region this endpoint is located
        :param weight: Endpoint weight across all endpoints in the group. Must be a value between 0 and 255. Default: 128
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_id": endpoint_id,
        }
        if preserve_client_ip is not None:
            self._values["preserve_client_ip"] = preserve_client_ip
        if region is not None:
            self._values["region"] = region
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def endpoint_id(self) -> builtins.str:
        '''Identifier of the endpoint.

        Load balancer ARN, instance ID or EIP allocation ID.
        '''
        result = self._values.get("endpoint_id")
        assert result is not None, "Required property 'endpoint_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preserve_client_ip(self) -> typing.Optional[builtins.bool]:
        '''Forward the client IP address.

        GlobalAccelerator will create Network Interfaces in your VPC in order
        to preserve the client IP address.

        Only applies to Application Load Balancers and EC2 instances.

        Client IP address preservation is supported only in specific AWS Regions.
        See the GlobalAccelerator Developer Guide for a list.

        :default: true if possible and available
        '''
        result = self._values.get("preserve_client_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region where this endpoint is located.

        :default: - Unknown what region this endpoint is located
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Endpoint weight across all endpoints in the group.

        Must be a value between 0 and 255.

        :default: 128
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RawEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAccelerator)
class Accelerator(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.Accelerator",
):
    '''The Accelerator construct.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        accelerator_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param accelerator_name: The name of the accelerator. Default: - resource ID
        :param enabled: Indicates whether the accelerator is enabled. Default: true
        '''
        props = AcceleratorProps(accelerator_name=accelerator_name, enabled=enabled)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAcceleratorAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_accelerator_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        accelerator_arn: builtins.str,
        dns_name: builtins.str,
    ) -> IAccelerator:
        '''import from attributes.

        :param scope: -
        :param id: -
        :param accelerator_arn: The ARN of the accelerator.
        :param dns_name: The DNS name of the accelerator.
        '''
        attrs = AcceleratorAttributes(
            accelerator_arn=accelerator_arn, dns_name=dns_name
        )

        return typing.cast(IAccelerator, jsii.sinvoke(cls, "fromAcceleratorAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addListener")
    def add_listener(
        self,
        id: builtins.str,
        *,
        port_ranges: typing.Sequence[PortRange],
        client_affinity: typing.Optional[ClientAffinity] = None,
        listener_name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[ConnectionProtocol] = None,
    ) -> Listener:
        '''Add a listener to the accelerator.

        :param id: -
        :param port_ranges: The list of port ranges for the connections from clients to the accelerator.
        :param client_affinity: Client affinity to direct all requests from a user to the same endpoint. If you have stateful applications, client affinity lets you direct all requests from a user to the same endpoint. By default, each connection from each client is routed to seperate endpoints. Set client affinity to SOURCE_IP to route all connections from a single client to the same endpoint. Default: ClientAffinity.NONE
        :param listener_name: Name of the listener. Default: - logical ID of the resource
        :param protocol: The protocol for the connections from clients to the accelerator. Default: ConnectionProtocol.TCP
        '''
        options = ListenerOptions(
            port_ranges=port_ranges,
            client_affinity=client_affinity,
            listener_name=listener_name,
            protocol=protocol,
        )

        return typing.cast(Listener, jsii.invoke(self, "addListener", [id, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="acceleratorArn")
    def accelerator_arn(self) -> builtins.str:
        '''The ARN of the accelerator.'''
        return typing.cast(builtins.str, jsii.get(self, "acceleratorArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        '''The Domain Name System (DNS) name that Global Accelerator creates that points to your accelerator's static IP addresses.'''
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))


@jsii.implements(IEndpointGroup)
class EndpointGroup(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-globalaccelerator.EndpointGroup",
):
    '''EndpointGroup construct.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        listener: IListener,
        endpoint_group_name: typing.Optional[builtins.str] = None,
        endpoints: typing.Optional[typing.Sequence[IEndpoint]] = None,
        health_check_interval: typing.Optional[aws_cdk.core.Duration] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[jsii.Number] = None,
        health_check_protocol: typing.Optional[HealthCheckProtocol] = None,
        health_check_threshold: typing.Optional[jsii.Number] = None,
        port_overrides: typing.Optional[typing.Sequence[PortOverride]] = None,
        region: typing.Optional[builtins.str] = None,
        traffic_dial_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param listener: The Amazon Resource Name (ARN) of the listener.
        :param endpoint_group_name: Name of the endpoint group. Default: - logical ID of the resource
        :param endpoints: Initial list of endpoints for this group. Default: - Group is initially empty
        :param health_check_interval: The time between health checks for each endpoint. Must be either 10 or 30 seconds. Default: Duration.seconds(30)
        :param health_check_path: The ping path for health checks (if the protocol is HTTP(S)). Default: '/'
        :param health_check_port: The port used to perform health checks. Default: - The listener's port
        :param health_check_protocol: The protocol used to perform health checks. Default: HealthCheckProtocol.TCP
        :param health_check_threshold: The number of consecutive health checks required to set the state of a healthy endpoint to unhealthy, or to set an unhealthy endpoint to healthy. Default: 3
        :param port_overrides: Override the destination ports used to route traffic to an endpoint. Unless overridden, the port used to hit the endpoint will be the same as the port that traffic arrives on at the listener. Default: - No overrides
        :param region: The AWS Region where the endpoint group is located. Default: - region of the first endpoint in this group, or the stack region if that region can't be determined
        :param traffic_dial_percentage: The percentage of traffic to send to this AWS Region. The percentage is applied to the traffic that would otherwise have been routed to the Region based on optimal routing. Additional traffic is distributed to other endpoint groups for this listener. Default: 100
        '''
        props = EndpointGroupProps(
            listener=listener,
            endpoint_group_name=endpoint_group_name,
            endpoints=endpoints,
            health_check_interval=health_check_interval,
            health_check_path=health_check_path,
            health_check_port=health_check_port,
            health_check_protocol=health_check_protocol,
            health_check_threshold=health_check_threshold,
            port_overrides=port_overrides,
            region=region,
            traffic_dial_percentage=traffic_dial_percentage,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromEndpointGroupArn") # type: ignore[misc]
    @builtins.classmethod
    def from_endpoint_group_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        endpoint_group_arn: builtins.str,
    ) -> IEndpointGroup:
        '''import from ARN.

        :param scope: -
        :param id: -
        :param endpoint_group_arn: -
        '''
        return typing.cast(IEndpointGroup, jsii.sinvoke(cls, "fromEndpointGroupArn", [scope, id, endpoint_group_arn]))

    @jsii.member(jsii_name="addEndpoint")
    def add_endpoint(self, endpoint: IEndpoint) -> None:
        '''Add an endpoint.

        :param endpoint: -
        '''
        return typing.cast(None, jsii.invoke(self, "addEndpoint", [endpoint]))

    @jsii.member(jsii_name="connectionsPeer")
    def connections_peer(
        self,
        id: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> aws_cdk.aws_ec2.IPeer:
        '''Return an object that represents the Accelerator's Security Group.

        Uses a Custom Resource to look up the Security Group that Accelerator
        creates at deploy time. Requires your VPC ID to perform the lookup.

        The Security Group will only be created if you enable **Client IP
        Preservation** on any of the endpoints.

        You cannot manipulate the rules inside this security group, but you can
        use this security group as a Peer in Connections rules on other
        constructs.

        :param id: -
        :param vpc: -
        '''
        return typing.cast(aws_cdk.aws_ec2.IPeer, jsii.invoke(self, "connectionsPeer", [id, vpc]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointGroupArn")
    def endpoint_group_arn(self) -> builtins.str:
        '''EndpointGroup ARN.'''
        return typing.cast(builtins.str, jsii.get(self, "endpointGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpointGroupName")
    def endpoint_group_name(self) -> builtins.str:
        '''The name of the endpoint group.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "endpointGroupName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="endpoints")
    def _endpoints(self) -> typing.List[IEndpoint]:
        '''The array of the endpoints in this endpoint group.'''
        return typing.cast(typing.List[IEndpoint], jsii.get(self, "endpoints"))


__all__ = [
    "Accelerator",
    "AcceleratorAttributes",
    "AcceleratorProps",
    "CfnAccelerator",
    "CfnAcceleratorProps",
    "CfnEndpointGroup",
    "CfnEndpointGroupProps",
    "CfnListener",
    "CfnListenerProps",
    "ClientAffinity",
    "ConnectionProtocol",
    "EndpointGroup",
    "EndpointGroupOptions",
    "EndpointGroupProps",
    "HealthCheckProtocol",
    "IAccelerator",
    "IEndpoint",
    "IEndpointGroup",
    "IListener",
    "Listener",
    "ListenerOptions",
    "ListenerProps",
    "PortOverride",
    "PortRange",
    "RawEndpoint",
    "RawEndpointProps",
]

publication.publish()
