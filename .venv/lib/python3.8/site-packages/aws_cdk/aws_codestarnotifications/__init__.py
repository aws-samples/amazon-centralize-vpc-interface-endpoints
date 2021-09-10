'''
# AWS CodeStarNotifications Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## NotificationRule

The `NotificationRule` construct defines an AWS CodeStarNotifications rule.
The rule specifies the events you want notifications about and the targets
(such as Amazon SNS topics or AWS Chatbot clients configured for Slack)
where you want to receive them.
Notification targets are objects that implement the `INotificationRuleTarget`
interface and notification source is object that implement the `INotificationRuleSource` interface.

## Notification Targets

This module includes classes that implement the `INotificationRuleTarget` interface for SNS and slack in AWS Chatbot.

The following targets are supported:

* `SNS`: specify event and notify to SNS topic.
* `AWS Chatbot`: specify event and notify to slack channel and only support `SlackChannelConfiguration`.

## Examples

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codestarnotifications as notifications
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_sns as sns
import aws_cdk.aws_chatbot as chatbot

project = codebuild.PipelineProject(stack, "MyProject")

topic = sns.Topic(stack, "MyTopic1")

slack = chatbot.SlackChannelConfiguration(stack, "MySlackChannel",
    slack_channel_configuration_name="YOUR_CHANNEL_NAME",
    slack_workspace_id="YOUR_SLACK_WORKSPACE_ID",
    slack_channel_id="YOUR_SLACK_CHANNEL_ID"
)

rule = notifications.NotificationRule(stack, "NotificationRule",
    source=project,
    events=["codebuild-project-build-state-succeeded", "codebuild-project-build-state-failed"
    ],
    targets=[topic]
)
rule.add_target(slack)
```

## Notification Source

This module includes classes that implement the `INotificationRuleSource` interface for AWS CodeBuild,
AWS CodePipeline and will support AWS CodeCommit, AWS CodeDeploy in future.

The following sources are supported:

* `AWS CodeBuild`: support codebuild project to trigger notification when event specified.
* `AWS CodePipeline`: support codepipeline to trigger notification when event specified.

## Events

For the complete list of supported event types for CodeBuild and CodePipeline, see:

* [Events for notification rules on build projects](https://docs.aws.amazon.com/dtconsole/latest/userguide/concepts.html#events-ref-buildproject).
* [Events for notification rules on pipelines](https://docs.aws.amazon.com/dtconsole/latest/userguide/concepts.html#events-ref-pipeline).
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

import aws_cdk.core
import constructs


@jsii.implements(aws_cdk.core.IInspectable)
class CfnNotificationRule(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codestarnotifications.CfnNotificationRule",
):
    '''A CloudFormation ``AWS::CodeStarNotifications::NotificationRule``.

    :cloudformationResource: AWS::CodeStarNotifications::NotificationRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        detail_type: builtins.str,
        event_type_ids: typing.Sequence[builtins.str],
        name: builtins.str,
        resource: builtins.str,
        targets: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union["CfnNotificationRule.TargetProperty", aws_cdk.core.IResolvable]]],
        status: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::CodeStarNotifications::NotificationRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param detail_type: ``AWS::CodeStarNotifications::NotificationRule.DetailType``.
        :param event_type_ids: ``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.
        :param name: ``AWS::CodeStarNotifications::NotificationRule.Name``.
        :param resource: ``AWS::CodeStarNotifications::NotificationRule.Resource``.
        :param targets: ``AWS::CodeStarNotifications::NotificationRule.Targets``.
        :param status: ``AWS::CodeStarNotifications::NotificationRule.Status``.
        :param tags: ``AWS::CodeStarNotifications::NotificationRule.Tags``.
        '''
        props = CfnNotificationRuleProps(
            detail_type=detail_type,
            event_type_ids=event_type_ids,
            name=name,
            resource=resource,
            targets=targets,
            status=status,
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::CodeStarNotifications::NotificationRule.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="detailType")
    def detail_type(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.DetailType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-detailtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "detailType"))

    @detail_type.setter
    def detail_type(self, value: builtins.str) -> None:
        jsii.set(self, "detailType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventTypeIds")
    def event_type_ids(self) -> typing.List[builtins.str]:
        '''``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-eventtypeids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventTypeIds"))

    @event_type_ids.setter
    def event_type_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "eventTypeIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resource")
    def resource(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.Resource``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-resource
        '''
        return typing.cast(builtins.str, jsii.get(self, "resource"))

    @resource.setter
    def resource(self, value: builtins.str) -> None:
        jsii.set(self, "resource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnNotificationRule.TargetProperty", aws_cdk.core.IResolvable]]]:
        '''``AWS::CodeStarNotifications::NotificationRule.Targets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-targets
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnNotificationRule.TargetProperty", aws_cdk.core.IResolvable]]], jsii.get(self, "targets"))

    @targets.setter
    def targets(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnNotificationRule.TargetProperty", aws_cdk.core.IResolvable]]],
    ) -> None:
        jsii.set(self, "targets", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeStarNotifications::NotificationRule.Status``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codestarnotifications.CfnNotificationRule.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"target_address": "targetAddress", "target_type": "targetType"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            target_address: typing.Optional[builtins.str] = None,
            target_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param target_address: ``CfnNotificationRule.TargetProperty.TargetAddress``.
            :param target_type: ``CfnNotificationRule.TargetProperty.TargetType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if target_address is not None:
                self._values["target_address"] = target_address
            if target_type is not None:
                self._values["target_type"] = target_type

        @builtins.property
        def target_address(self) -> typing.Optional[builtins.str]:
            '''``CfnNotificationRule.TargetProperty.TargetAddress``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html#cfn-codestarnotifications-notificationrule-target-targetaddress
            '''
            result = self._values.get("target_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_type(self) -> typing.Optional[builtins.str]:
            '''``CfnNotificationRule.TargetProperty.TargetType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestarnotifications-notificationrule-target.html#cfn-codestarnotifications-notificationrule-target-targettype
            '''
            result = self._values.get("target_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codestarnotifications.CfnNotificationRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "detail_type": "detailType",
        "event_type_ids": "eventTypeIds",
        "name": "name",
        "resource": "resource",
        "targets": "targets",
        "status": "status",
        "tags": "tags",
    },
)
class CfnNotificationRuleProps:
    def __init__(
        self,
        *,
        detail_type: builtins.str,
        event_type_ids: typing.Sequence[builtins.str],
        name: builtins.str,
        resource: builtins.str,
        targets: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[CfnNotificationRule.TargetProperty, aws_cdk.core.IResolvable]]],
        status: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``AWS::CodeStarNotifications::NotificationRule``.

        :param detail_type: ``AWS::CodeStarNotifications::NotificationRule.DetailType``.
        :param event_type_ids: ``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.
        :param name: ``AWS::CodeStarNotifications::NotificationRule.Name``.
        :param resource: ``AWS::CodeStarNotifications::NotificationRule.Resource``.
        :param targets: ``AWS::CodeStarNotifications::NotificationRule.Targets``.
        :param status: ``AWS::CodeStarNotifications::NotificationRule.Status``.
        :param tags: ``AWS::CodeStarNotifications::NotificationRule.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "detail_type": detail_type,
            "event_type_ids": event_type_ids,
            "name": name,
            "resource": resource,
            "targets": targets,
        }
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def detail_type(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.DetailType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-detailtype
        '''
        result = self._values.get("detail_type")
        assert result is not None, "Required property 'detail_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_type_ids(self) -> typing.List[builtins.str]:
        '''``AWS::CodeStarNotifications::NotificationRule.EventTypeIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-eventtypeids
        '''
        result = self._values.get("event_type_ids")
        assert result is not None, "Required property 'event_type_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource(self) -> builtins.str:
        '''``AWS::CodeStarNotifications::NotificationRule.Resource``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-resource
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[CfnNotificationRule.TargetProperty, aws_cdk.core.IResolvable]]]:
        '''``AWS::CodeStarNotifications::NotificationRule.Targets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-targets
        '''
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[CfnNotificationRule.TargetProperty, aws_cdk.core.IResolvable]]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeStarNotifications::NotificationRule.Status``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''``AWS::CodeStarNotifications::NotificationRule.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-codestarnotifications.DetailType")
class DetailType(enum.Enum):
    '''The level of detail to include in the notifications for this resource.'''

    BASIC = "BASIC"
    '''BASIC will include only the contents of the event as it would appear in AWS CloudWatch.'''
    FULL = "FULL"
    '''FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created.'''


@jsii.interface(jsii_type="@aws-cdk/aws-codestarnotifications.INotificationRule")
class INotificationRule(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''Represents a notification rule.'''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationRuleArn")
    def notification_rule_arn(self) -> builtins.str:
        '''The ARN of the notification rule (i.e. arn:aws:codestar-notifications:::notificationrule/01234abcde).

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: "INotificationRuleTarget") -> builtins.bool:
        '''Adds target to notification rule.

        :param target: The SNS topic or AWS Chatbot Slack target.

        :return: boolean - return true if it had any effect
        '''
        ...


class _INotificationRuleProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''Represents a notification rule.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codestarnotifications.INotificationRule"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationRuleArn")
    def notification_rule_arn(self) -> builtins.str:
        '''The ARN of the notification rule (i.e. arn:aws:codestar-notifications:::notificationrule/01234abcde).

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "notificationRuleArn"))

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: "INotificationRuleTarget") -> builtins.bool:
        '''Adds target to notification rule.

        :param target: The SNS topic or AWS Chatbot Slack target.

        :return: boolean - return true if it had any effect
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "addTarget", [target]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INotificationRule).__jsii_proxy_class__ = lambda : _INotificationRuleProxy


@jsii.interface(jsii_type="@aws-cdk/aws-codestarnotifications.INotificationRuleSource")
class INotificationRuleSource(typing_extensions.Protocol):
    '''Represents a notification source The source that allows CodeBuild and CodePipeline to associate with this rule.'''

    @jsii.member(jsii_name="bindAsNotificationRuleSource")
    def bind_as_notification_rule_source(
        self,
        scope: constructs.Construct,
    ) -> "NotificationRuleSourceConfig":
        '''Returns a source configuration for notification rule.

        :param scope: -
        '''
        ...


class _INotificationRuleSourceProxy:
    '''Represents a notification source The source that allows CodeBuild and CodePipeline to associate with this rule.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codestarnotifications.INotificationRuleSource"

    @jsii.member(jsii_name="bindAsNotificationRuleSource")
    def bind_as_notification_rule_source(
        self,
        scope: constructs.Construct,
    ) -> "NotificationRuleSourceConfig":
        '''Returns a source configuration for notification rule.

        :param scope: -
        '''
        return typing.cast("NotificationRuleSourceConfig", jsii.invoke(self, "bindAsNotificationRuleSource", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INotificationRuleSource).__jsii_proxy_class__ = lambda : _INotificationRuleSourceProxy


@jsii.interface(jsii_type="@aws-cdk/aws-codestarnotifications.INotificationRuleTarget")
class INotificationRuleTarget(typing_extensions.Protocol):
    '''Represents a notification target That allows AWS Chatbot and SNS topic to associate with this rule target.'''

    @jsii.member(jsii_name="bindAsNotificationRuleTarget")
    def bind_as_notification_rule_target(
        self,
        scope: constructs.Construct,
    ) -> "NotificationRuleTargetConfig":
        '''Returns a target configuration for notification rule.

        :param scope: -
        '''
        ...


class _INotificationRuleTargetProxy:
    '''Represents a notification target That allows AWS Chatbot and SNS topic to associate with this rule target.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codestarnotifications.INotificationRuleTarget"

    @jsii.member(jsii_name="bindAsNotificationRuleTarget")
    def bind_as_notification_rule_target(
        self,
        scope: constructs.Construct,
    ) -> "NotificationRuleTargetConfig":
        '''Returns a target configuration for notification rule.

        :param scope: -
        '''
        return typing.cast("NotificationRuleTargetConfig", jsii.invoke(self, "bindAsNotificationRuleTarget", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INotificationRuleTarget).__jsii_proxy_class__ = lambda : _INotificationRuleTargetProxy


@jsii.implements(INotificationRule)
class NotificationRule(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codestarnotifications.NotificationRule",
):
    '''A new notification rule.

    :resource: AWS::CodeStarNotifications::NotificationRule
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        events: typing.Sequence[builtins.str],
        source: INotificationRuleSource,
        targets: typing.Optional[typing.Sequence[INotificationRuleTarget]] = None,
        detail_type: typing.Optional[DetailType] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param events: A list of event types associated with this notification rule. For a complete list of event types and IDs, see Notification concepts in the Developer Tools Console User Guide.
        :param source: The Amazon Resource Name (ARN) of the resource to associate with the notification rule. Currently, Supported sources include pipelines in AWS CodePipeline, build projects in AWS CodeBuild, and repositories in AWS CodeCommit in this L2 constructor.
        :param targets: The targets to register for the notification destination. Default: - No targets are added to the rule. Use ``addTarget()`` to add a target.
        :param detail_type: The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``
        '''
        props = NotificationRuleProps(
            events=events,
            source=source,
            targets=targets,
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromNotificationRuleArn") # type: ignore[misc]
    @builtins.classmethod
    def from_notification_rule_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        notification_rule_arn: builtins.str,
    ) -> INotificationRule:
        '''Import an existing notification rule provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param notification_rule_arn: Notification rule ARN (i.e. arn:aws:codestar-notifications:::notificationrule/01234abcde).
        '''
        return typing.cast(INotificationRule, jsii.sinvoke(cls, "fromNotificationRuleArn", [scope, id, notification_rule_arn]))

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: INotificationRuleTarget) -> builtins.bool:
        '''Adds target to notification rule.

        :param target: The SNS topic or AWS Chatbot Slack target.
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "addTarget", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationRuleArn")
    def notification_rule_arn(self) -> builtins.str:
        '''The ARN of the notification rule (i.e. arn:aws:codestar-notifications:::notificationrule/01234abcde).

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "notificationRuleArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codestarnotifications.NotificationRuleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "detail_type": "detailType",
        "enabled": "enabled",
        "notification_rule_name": "notificationRuleName",
    },
)
class NotificationRuleOptions:
    def __init__(
        self,
        *,
        detail_type: typing.Optional[DetailType] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Standard set of options for ``notifyOnXxx`` codestar notification handler on construct.

        :param detail_type: The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if detail_type is not None:
            self._values["detail_type"] = detail_type
        if enabled is not None:
            self._values["enabled"] = enabled
        if notification_rule_name is not None:
            self._values["notification_rule_name"] = notification_rule_name

    @builtins.property
    def detail_type(self) -> typing.Optional[DetailType]:
        '''The level of detail to include in the notifications for this resource.

        BASIC will include only the contents of the event as it would appear in AWS CloudWatch.
        FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created.

        :default: DetailType.FULL
        '''
        result = self._values.get("detail_type")
        return typing.cast(typing.Optional[DetailType], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''The status of the notification rule.

        If the enabled is set to DISABLED, notifications aren't sent for the notification rule.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notification_rule_name(self) -> typing.Optional[builtins.str]:
        '''The name for the notification rule.

        Notification rule names must be unique in your AWS account.

        :default: - generated from the ``id``
        '''
        result = self._values.get("notification_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationRuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codestarnotifications.NotificationRuleProps",
    jsii_struct_bases=[NotificationRuleOptions],
    name_mapping={
        "detail_type": "detailType",
        "enabled": "enabled",
        "notification_rule_name": "notificationRuleName",
        "events": "events",
        "source": "source",
        "targets": "targets",
    },
)
class NotificationRuleProps(NotificationRuleOptions):
    def __init__(
        self,
        *,
        detail_type: typing.Optional[DetailType] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
        events: typing.Sequence[builtins.str],
        source: INotificationRuleSource,
        targets: typing.Optional[typing.Sequence[INotificationRuleTarget]] = None,
    ) -> None:
        '''Properties for a new notification rule.

        :param detail_type: The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``
        :param events: A list of event types associated with this notification rule. For a complete list of event types and IDs, see Notification concepts in the Developer Tools Console User Guide.
        :param source: The Amazon Resource Name (ARN) of the resource to associate with the notification rule. Currently, Supported sources include pipelines in AWS CodePipeline, build projects in AWS CodeBuild, and repositories in AWS CodeCommit in this L2 constructor.
        :param targets: The targets to register for the notification destination. Default: - No targets are added to the rule. Use ``addTarget()`` to add a target.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "events": events,
            "source": source,
        }
        if detail_type is not None:
            self._values["detail_type"] = detail_type
        if enabled is not None:
            self._values["enabled"] = enabled
        if notification_rule_name is not None:
            self._values["notification_rule_name"] = notification_rule_name
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def detail_type(self) -> typing.Optional[DetailType]:
        '''The level of detail to include in the notifications for this resource.

        BASIC will include only the contents of the event as it would appear in AWS CloudWatch.
        FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created.

        :default: DetailType.FULL
        '''
        result = self._values.get("detail_type")
        return typing.cast(typing.Optional[DetailType], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''The status of the notification rule.

        If the enabled is set to DISABLED, notifications aren't sent for the notification rule.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notification_rule_name(self) -> typing.Optional[builtins.str]:
        '''The name for the notification rule.

        Notification rule names must be unique in your AWS account.

        :default: - generated from the ``id``
        '''
        result = self._values.get("notification_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def events(self) -> typing.List[builtins.str]:
        '''A list of event types associated with this notification rule.

        For a complete list of event types and IDs, see Notification concepts in the Developer Tools Console User Guide.

        :see: https://docs.aws.amazon.com/dtconsole/latest/userguide/concepts.html#concepts-api
        '''
        result = self._values.get("events")
        assert result is not None, "Required property 'events' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def source(self) -> INotificationRuleSource:
        '''The Amazon Resource Name (ARN) of the resource to associate with the notification rule.

        Currently, Supported sources include pipelines in AWS CodePipeline, build projects in AWS CodeBuild, and repositories in AWS CodeCommit in this L2 constructor.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarnotifications-notificationrule.html#cfn-codestarnotifications-notificationrule-resource
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(INotificationRuleSource, result)

    @builtins.property
    def targets(self) -> typing.Optional[typing.List[INotificationRuleTarget]]:
        '''The targets to register for the notification destination.

        :default: - No targets are added to the rule. Use ``addTarget()`` to add a target.
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.List[INotificationRuleTarget]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codestarnotifications.NotificationRuleSourceConfig",
    jsii_struct_bases=[],
    name_mapping={"source_arn": "sourceArn"},
)
class NotificationRuleSourceConfig:
    def __init__(self, *, source_arn: builtins.str) -> None:
        '''Information about the Codebuild or CodePipeline associated with a notification source.

        :param source_arn: The Amazon Resource Name (ARN) of the notification source.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "source_arn": source_arn,
        }

    @builtins.property
    def source_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the notification source.'''
        result = self._values.get("source_arn")
        assert result is not None, "Required property 'source_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationRuleSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codestarnotifications.NotificationRuleTargetConfig",
    jsii_struct_bases=[],
    name_mapping={"target_address": "targetAddress", "target_type": "targetType"},
)
class NotificationRuleTargetConfig:
    def __init__(
        self,
        *,
        target_address: builtins.str,
        target_type: builtins.str,
    ) -> None:
        '''Information about the SNS topic or AWS Chatbot client associated with a notification target.

        :param target_address: The Amazon Resource Name (ARN) of the Amazon SNS topic or AWS Chatbot client.
        :param target_type: The target type. Can be an Amazon SNS topic or AWS Chatbot client.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "target_address": target_address,
            "target_type": target_type,
        }

    @builtins.property
    def target_address(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic or AWS Chatbot client.'''
        result = self._values.get("target_address")
        assert result is not None, "Required property 'target_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_type(self) -> builtins.str:
        '''The target type.

        Can be an Amazon SNS topic or AWS Chatbot client.
        '''
        result = self._values.get("target_type")
        assert result is not None, "Required property 'target_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationRuleTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnNotificationRule",
    "CfnNotificationRuleProps",
    "DetailType",
    "INotificationRule",
    "INotificationRuleSource",
    "INotificationRuleTarget",
    "NotificationRule",
    "NotificationRuleOptions",
    "NotificationRuleProps",
    "NotificationRuleSourceConfig",
    "NotificationRuleTargetConfig",
]

publication.publish()
