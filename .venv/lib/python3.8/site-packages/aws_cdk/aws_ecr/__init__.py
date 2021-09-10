'''
# Amazon ECR Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This package contains constructs for working with Amazon Elastic Container Registry.

## Repositories

Define a repository by creating a new instance of `Repository`. A repository
holds multiple verions of a single container image.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
repository = ecr.Repository(self, "Repository")
```

## Image scanning

Amazon ECR image scanning helps in identifying software vulnerabilities in your container images. You can manually scan container images stored in Amazon ECR, or you can configure your repositories to scan images when you push them to a repository. To create a new repository to scan on push, simply enable `imageScanOnPush` in the properties

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
repository = ecr.Repository(stack, "Repo",
    image_scan_on_push=True
)
```

To create an `onImageScanCompleted` event rule and trigger the event target

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
repository.on_image_scan_completed("ImageScanComplete").add_target(...)
```

### Authorization Token

Besides the Amazon ECR APIs, ECR also allows the Docker CLI or a language-specific Docker library to push and pull
images from an ECR repository. However, the Docker CLI does not support native IAM authentication methods and
additional steps must be taken so that Amazon ECR can authenticate and authorize Docker push and pull requests.
More information can be found at at [Registry Authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth).

A Docker authorization token can be obtained using the `GetAuthorizationToken` ECR API. The following code snippets
grants an IAM user access to call this API.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ecr as ecr

user = iam.User(self, "User", ...)
ecr.AuthorizationToken.grant_read(user)
```

If you access images in the [Public ECR Gallery](https://gallery.ecr.aws/) as well, it is recommended you authenticate to the registry to benefit from
higher rate and bandwidth limits.

> See `Pricing` in https://aws.amazon.com/blogs/aws/amazon-ecr-public-a-new-public-container-registry/ and [Service quotas](https://docs.aws.amazon.com/AmazonECR/latest/public/public-service-quotas.html).

The following code snippet grants an IAM user access to retrieve an authorization token for the public gallery.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ecr as ecr

user = iam.User(self, "User", ...)
ecr.PublicGalleryAuthorizationToken.grant_read(user)
```

This user can then proceed to login to the registry using one of the [authentication methods](https://docs.aws.amazon.com/AmazonECR/latest/public/public-registries.html#public-registry-auth).

### Image tag immutability

You can set tag immutability on images in our repository using the `imageTagMutability` construct prop.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
ecr.Repository(stack, "Repo", image_tag_mutability=ecr.TagMutability.IMMUTABLE)
```

## Automatically clean up repositories

You can set life cycle rules to automatically clean up old images from your
repository. The first life cycle rule that matches an image will be applied
against that image. For example, the following deletes images older than
30 days, while keeping all images tagged with prod (note that the order
is important here):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
repository.add_lifecycle_rule(tag_prefix_list=["prod"], max_image_count=9999)
repository.add_lifecycle_rule(max_image_age=cdk.Duration.days(30))
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

import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.core
import constructs


class AuthorizationToken(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr.AuthorizationToken",
):
    '''Authorization token to access private ECR repositories in the current environment via Docker CLI.

    :see: https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html
    '''

    @jsii.member(jsii_name="grantRead") # type: ignore[misc]
    @builtins.classmethod
    def grant_read(cls, grantee: aws_cdk.aws_iam.IGrantable) -> None:
        '''Grant access to retrieve an authorization token.

        :param grantee: -
        '''
        return typing.cast(None, jsii.sinvoke(cls, "grantRead", [grantee]))


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPublicRepository(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr.CfnPublicRepository",
):
    '''A CloudFormation ``AWS::ECR::PublicRepository``.

    :cloudformationResource: AWS::ECR::PublicRepository
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        repository_catalog_data: typing.Any = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::ECR::PublicRepository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param repository_catalog_data: ``AWS::ECR::PublicRepository.RepositoryCatalogData``.
        :param repository_name: ``AWS::ECR::PublicRepository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::PublicRepository.RepositoryPolicyText``.
        :param tags: ``AWS::ECR::PublicRepository.Tags``.
        '''
        props = CfnPublicRepositoryProps(
            repository_catalog_data=repository_catalog_data,
            repository_name=repository_name,
            repository_policy_text=repository_policy_text,
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::ECR::PublicRepository.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryCatalogData")
    def repository_catalog_data(self) -> typing.Any:
        '''``AWS::ECR::PublicRepository.RepositoryCatalogData``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositorycatalogdata
        '''
        return typing.cast(typing.Any, jsii.get(self, "repositoryCatalogData"))

    @repository_catalog_data.setter
    def repository_catalog_data(self, value: typing.Any) -> None:
        jsii.set(self, "repositoryCatalogData", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryPolicyText")
    def repository_policy_text(self) -> typing.Any:
        '''``AWS::ECR::PublicRepository.RepositoryPolicyText``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositorypolicytext
        '''
        return typing.cast(typing.Any, jsii.get(self, "repositoryPolicyText"))

    @repository_policy_text.setter
    def repository_policy_text(self, value: typing.Any) -> None:
        jsii.set(self, "repositoryPolicyText", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::ECR::PublicRepository.RepositoryName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositoryname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "repositoryName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.CfnPublicRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository_catalog_data": "repositoryCatalogData",
        "repository_name": "repositoryName",
        "repository_policy_text": "repositoryPolicyText",
        "tags": "tags",
    },
)
class CfnPublicRepositoryProps:
    def __init__(
        self,
        *,
        repository_catalog_data: typing.Any = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::ECR::PublicRepository``.

        :param repository_catalog_data: ``AWS::ECR::PublicRepository.RepositoryCatalogData``.
        :param repository_name: ``AWS::ECR::PublicRepository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::PublicRepository.RepositoryPolicyText``.
        :param tags: ``AWS::ECR::PublicRepository.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if repository_catalog_data is not None:
            self._values["repository_catalog_data"] = repository_catalog_data
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if repository_policy_text is not None:
            self._values["repository_policy_text"] = repository_policy_text
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def repository_catalog_data(self) -> typing.Any:
        '''``AWS::ECR::PublicRepository.RepositoryCatalogData``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositorycatalogdata
        '''
        result = self._values.get("repository_catalog_data")
        return typing.cast(typing.Any, result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::ECR::PublicRepository.RepositoryName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositoryname
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_policy_text(self) -> typing.Any:
        '''``AWS::ECR::PublicRepository.RepositoryPolicyText``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-repositorypolicytext
        '''
        result = self._values.get("repository_policy_text")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::ECR::PublicRepository.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-publicrepository.html#cfn-ecr-publicrepository-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublicRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRegistryPolicy(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr.CfnRegistryPolicy",
):
    '''A CloudFormation ``AWS::ECR::RegistryPolicy``.

    :cloudformationResource: AWS::ECR::RegistryPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registrypolicy.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        policy_text: typing.Any,
    ) -> None:
        '''Create a new ``AWS::ECR::RegistryPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_text: ``AWS::ECR::RegistryPolicy.PolicyText``.
        '''
        props = CfnRegistryPolicyProps(policy_text=policy_text)

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
    @jsii.member(jsii_name="attrRegistryId")
    def attr_registry_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: RegistryId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRegistryId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyText")
    def policy_text(self) -> typing.Any:
        '''``AWS::ECR::RegistryPolicy.PolicyText``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registrypolicy.html#cfn-ecr-registrypolicy-policytext
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyText"))

    @policy_text.setter
    def policy_text(self, value: typing.Any) -> None:
        jsii.set(self, "policyText", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.CfnRegistryPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy_text": "policyText"},
)
class CfnRegistryPolicyProps:
    def __init__(self, *, policy_text: typing.Any) -> None:
        '''Properties for defining a ``AWS::ECR::RegistryPolicy``.

        :param policy_text: ``AWS::ECR::RegistryPolicy.PolicyText``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registrypolicy.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "policy_text": policy_text,
        }

    @builtins.property
    def policy_text(self) -> typing.Any:
        '''``AWS::ECR::RegistryPolicy.PolicyText``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-registrypolicy.html#cfn-ecr-registrypolicy-policytext
        '''
        result = self._values.get("policy_text")
        assert result is not None, "Required property 'policy_text' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegistryPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnReplicationConfiguration(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr.CfnReplicationConfiguration",
):
    '''A CloudFormation ``AWS::ECR::ReplicationConfiguration``.

    :cloudformationResource: AWS::ECR::ReplicationConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-replicationconfiguration.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        replication_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnReplicationConfiguration.ReplicationConfigurationProperty"],
    ) -> None:
        '''Create a new ``AWS::ECR::ReplicationConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param replication_configuration: ``AWS::ECR::ReplicationConfiguration.ReplicationConfiguration``.
        '''
        props = CfnReplicationConfigurationProps(
            replication_configuration=replication_configuration
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
    @jsii.member(jsii_name="attrRegistryId")
    def attr_registry_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: RegistryId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRegistryId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="replicationConfiguration")
    def replication_configuration(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, "CfnReplicationConfiguration.ReplicationConfigurationProperty"]:
        '''``AWS::ECR::ReplicationConfiguration.ReplicationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-replicationconfiguration.html#cfn-ecr-replicationconfiguration-replicationconfiguration
        '''
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, "CfnReplicationConfiguration.ReplicationConfigurationProperty"], jsii.get(self, "replicationConfiguration"))

    @replication_configuration.setter
    def replication_configuration(
        self,
        value: typing.Union[aws_cdk.core.IResolvable, "CfnReplicationConfiguration.ReplicationConfigurationProperty"],
    ) -> None:
        jsii.set(self, "replicationConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ecr.CfnReplicationConfiguration.ReplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class ReplicationConfigurationProperty:
        def __init__(
            self,
            *,
            rules: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnReplicationConfiguration.ReplicationRuleProperty"]]],
        ) -> None:
            '''
            :param rules: ``CfnReplicationConfiguration.ReplicationConfigurationProperty.Rules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "rules": rules,
            }

        @builtins.property
        def rules(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnReplicationConfiguration.ReplicationRuleProperty"]]]:
            '''``CfnReplicationConfiguration.ReplicationConfigurationProperty.Rules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationconfiguration.html#cfn-ecr-replicationconfiguration-replicationconfiguration-rules
            '''
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnReplicationConfiguration.ReplicationRuleProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ecr.CfnReplicationConfiguration.ReplicationDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"region": "region", "registry_id": "registryId"},
    )
    class ReplicationDestinationProperty:
        def __init__(self, *, region: builtins.str, registry_id: builtins.str) -> None:
            '''
            :param region: ``CfnReplicationConfiguration.ReplicationDestinationProperty.Region``.
            :param registry_id: ``CfnReplicationConfiguration.ReplicationDestinationProperty.RegistryId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationdestination.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "region": region,
                "registry_id": registry_id,
            }

        @builtins.property
        def region(self) -> builtins.str:
            '''``CfnReplicationConfiguration.ReplicationDestinationProperty.Region``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationdestination.html#cfn-ecr-replicationconfiguration-replicationdestination-region
            '''
            result = self._values.get("region")
            assert result is not None, "Required property 'region' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def registry_id(self) -> builtins.str:
            '''``CfnReplicationConfiguration.ReplicationDestinationProperty.RegistryId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationdestination.html#cfn-ecr-replicationconfiguration-replicationdestination-registryid
            '''
            result = self._values.get("registry_id")
            assert result is not None, "Required property 'registry_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ecr.CfnReplicationConfiguration.ReplicationRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"destinations": "destinations"},
    )
    class ReplicationRuleProperty:
        def __init__(
            self,
            *,
            destinations: typing.Union[aws_cdk.core.IResolvable, typing.Sequence[typing.Union[aws_cdk.core.IResolvable, "CfnReplicationConfiguration.ReplicationDestinationProperty"]]],
        ) -> None:
            '''
            :param destinations: ``CfnReplicationConfiguration.ReplicationRuleProperty.Destinations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationrule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "destinations": destinations,
            }

        @builtins.property
        def destinations(
            self,
        ) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnReplicationConfiguration.ReplicationDestinationProperty"]]]:
            '''``CfnReplicationConfiguration.ReplicationRuleProperty.Destinations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-replicationconfiguration-replicationrule.html#cfn-ecr-replicationconfiguration-replicationrule-destinations
            '''
            result = self._values.get("destinations")
            assert result is not None, "Required property 'destinations' is missing"
            return typing.cast(typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnReplicationConfiguration.ReplicationDestinationProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.CfnReplicationConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={"replication_configuration": "replicationConfiguration"},
)
class CfnReplicationConfigurationProps:
    def __init__(
        self,
        *,
        replication_configuration: typing.Union[aws_cdk.core.IResolvable, CfnReplicationConfiguration.ReplicationConfigurationProperty],
    ) -> None:
        '''Properties for defining a ``AWS::ECR::ReplicationConfiguration``.

        :param replication_configuration: ``AWS::ECR::ReplicationConfiguration.ReplicationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-replicationconfiguration.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "replication_configuration": replication_configuration,
        }

    @builtins.property
    def replication_configuration(
        self,
    ) -> typing.Union[aws_cdk.core.IResolvable, CfnReplicationConfiguration.ReplicationConfigurationProperty]:
        '''``AWS::ECR::ReplicationConfiguration.ReplicationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-replicationconfiguration.html#cfn-ecr-replicationconfiguration-replicationconfiguration
        '''
        result = self._values.get("replication_configuration")
        assert result is not None, "Required property 'replication_configuration' is missing"
        return typing.cast(typing.Union[aws_cdk.core.IResolvable, CfnReplicationConfiguration.ReplicationConfigurationProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRepository(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr.CfnRepository",
):
    '''A CloudFormation ``AWS::ECR::Repository``.

    :cloudformationResource: AWS::ECR::Repository
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        encryption_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.EncryptionConfigurationProperty"]] = None,
        image_scanning_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.ImageScanningConfigurationProperty"]] = None,
        image_tag_mutability: typing.Optional[builtins.str] = None,
        lifecycle_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.LifecyclePolicyProperty"]] = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::ECR::Repository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param encryption_configuration: ``AWS::ECR::Repository.EncryptionConfiguration``.
        :param image_scanning_configuration: ``AWS::ECR::Repository.ImageScanningConfiguration``.
        :param image_tag_mutability: ``AWS::ECR::Repository.ImageTagMutability``.
        :param lifecycle_policy: ``AWS::ECR::Repository.LifecyclePolicy``.
        :param repository_name: ``AWS::ECR::Repository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::Repository.RepositoryPolicyText``.
        :param tags: ``AWS::ECR::Repository.Tags``.
        '''
        props = CfnRepositoryProps(
            encryption_configuration=encryption_configuration,
            image_scanning_configuration=image_scanning_configuration,
            image_tag_mutability=image_tag_mutability,
            lifecycle_policy=lifecycle_policy,
            repository_name=repository_name,
            repository_policy_text=repository_policy_text,
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrRepositoryUri")
    def attr_repository_uri(self) -> builtins.str:
        '''
        :cloudformationAttribute: RepositoryUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRepositoryUri"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::ECR::Repository.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryPolicyText")
    def repository_policy_text(self) -> typing.Any:
        '''``AWS::ECR::Repository.RepositoryPolicyText``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositorypolicytext
        '''
        return typing.cast(typing.Any, jsii.get(self, "repositoryPolicyText"))

    @repository_policy_text.setter
    def repository_policy_text(self, value: typing.Any) -> None:
        jsii.set(self, "repositoryPolicyText", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.EncryptionConfigurationProperty"]]:
        '''``AWS::ECR::Repository.EncryptionConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-encryptionconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.EncryptionConfigurationProperty"]], jsii.get(self, "encryptionConfiguration"))

    @encryption_configuration.setter
    def encryption_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.EncryptionConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "encryptionConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageScanningConfiguration")
    def image_scanning_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.ImageScanningConfigurationProperty"]]:
        '''``AWS::ECR::Repository.ImageScanningConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagescanningconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.ImageScanningConfigurationProperty"]], jsii.get(self, "imageScanningConfiguration"))

    @image_scanning_configuration.setter
    def image_scanning_configuration(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.ImageScanningConfigurationProperty"]],
    ) -> None:
        jsii.set(self, "imageScanningConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageTagMutability")
    def image_tag_mutability(self) -> typing.Optional[builtins.str]:
        '''``AWS::ECR::Repository.ImageTagMutability``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagetagmutability
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageTagMutability"))

    @image_tag_mutability.setter
    def image_tag_mutability(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "imageTagMutability", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lifecyclePolicy")
    def lifecycle_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.LifecyclePolicyProperty"]]:
        '''``AWS::ECR::Repository.LifecyclePolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-lifecyclepolicy
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.LifecyclePolicyProperty"]], jsii.get(self, "lifecyclePolicy"))

    @lifecycle_policy.setter
    def lifecycle_policy(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnRepository.LifecyclePolicyProperty"]],
    ) -> None:
        jsii.set(self, "lifecyclePolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::ECR::Repository.RepositoryName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositoryname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "repositoryName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ecr.CfnRepository.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType", "kms_key": "kmsKey"},
    )
    class EncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            encryption_type: builtins.str,
            kms_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param encryption_type: ``CfnRepository.EncryptionConfigurationProperty.EncryptionType``.
            :param kms_key: ``CfnRepository.EncryptionConfigurationProperty.KmsKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-encryptionconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "encryption_type": encryption_type,
            }
            if kms_key is not None:
                self._values["kms_key"] = kms_key

        @builtins.property
        def encryption_type(self) -> builtins.str:
            '''``CfnRepository.EncryptionConfigurationProperty.EncryptionType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-encryptionconfiguration.html#cfn-ecr-repository-encryptionconfiguration-encryptiontype
            '''
            result = self._values.get("encryption_type")
            assert result is not None, "Required property 'encryption_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key(self) -> typing.Optional[builtins.str]:
            '''``CfnRepository.EncryptionConfigurationProperty.KmsKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-encryptionconfiguration.html#cfn-ecr-repository-encryptionconfiguration-kmskey
            '''
            result = self._values.get("kms_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ecr.CfnRepository.ImageScanningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"scan_on_push": "scanOnPush"},
    )
    class ImageScanningConfigurationProperty:
        def __init__(
            self,
            *,
            scan_on_push: typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]] = None,
        ) -> None:
            '''
            :param scan_on_push: ``CfnRepository.ImageScanningConfigurationProperty.ScanOnPush``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-imagescanningconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if scan_on_push is not None:
                self._values["scan_on_push"] = scan_on_push

        @builtins.property
        def scan_on_push(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]]:
            '''``CfnRepository.ImageScanningConfigurationProperty.ScanOnPush``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-imagescanningconfiguration.html#cfn-ecr-repository-imagescanningconfiguration-scanonpush
            '''
            result = self._values.get("scan_on_push")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, aws_cdk.core.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ImageScanningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ecr.CfnRepository.LifecyclePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lifecycle_policy_text": "lifecyclePolicyText",
            "registry_id": "registryId",
        },
    )
    class LifecyclePolicyProperty:
        def __init__(
            self,
            *,
            lifecycle_policy_text: typing.Optional[builtins.str] = None,
            registry_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param lifecycle_policy_text: ``CfnRepository.LifecyclePolicyProperty.LifecyclePolicyText``.
            :param registry_id: ``CfnRepository.LifecyclePolicyProperty.RegistryId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if lifecycle_policy_text is not None:
                self._values["lifecycle_policy_text"] = lifecycle_policy_text
            if registry_id is not None:
                self._values["registry_id"] = registry_id

        @builtins.property
        def lifecycle_policy_text(self) -> typing.Optional[builtins.str]:
            '''``CfnRepository.LifecyclePolicyProperty.LifecyclePolicyText``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-lifecyclepolicytext
            '''
            result = self._values.get("lifecycle_policy_text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def registry_id(self) -> typing.Optional[builtins.str]:
            '''``CfnRepository.LifecyclePolicyProperty.RegistryId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecr-repository-lifecyclepolicy.html#cfn-ecr-repository-lifecyclepolicy-registryid
            '''
            result = self._values.get("registry_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecyclePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.CfnRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_configuration": "encryptionConfiguration",
        "image_scanning_configuration": "imageScanningConfiguration",
        "image_tag_mutability": "imageTagMutability",
        "lifecycle_policy": "lifecyclePolicy",
        "repository_name": "repositoryName",
        "repository_policy_text": "repositoryPolicyText",
        "tags": "tags",
    },
)
class CfnRepositoryProps:
    def __init__(
        self,
        *,
        encryption_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.EncryptionConfigurationProperty]] = None,
        image_scanning_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.ImageScanningConfigurationProperty]] = None,
        image_tag_mutability: typing.Optional[builtins.str] = None,
        lifecycle_policy: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.LifecyclePolicyProperty]] = None,
        repository_name: typing.Optional[builtins.str] = None,
        repository_policy_text: typing.Any = None,
        tags: typing.Optional[typing.Sequence[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::ECR::Repository``.

        :param encryption_configuration: ``AWS::ECR::Repository.EncryptionConfiguration``.
        :param image_scanning_configuration: ``AWS::ECR::Repository.ImageScanningConfiguration``.
        :param image_tag_mutability: ``AWS::ECR::Repository.ImageTagMutability``.
        :param lifecycle_policy: ``AWS::ECR::Repository.LifecyclePolicy``.
        :param repository_name: ``AWS::ECR::Repository.RepositoryName``.
        :param repository_policy_text: ``AWS::ECR::Repository.RepositoryPolicyText``.
        :param tags: ``AWS::ECR::Repository.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if image_scanning_configuration is not None:
            self._values["image_scanning_configuration"] = image_scanning_configuration
        if image_tag_mutability is not None:
            self._values["image_tag_mutability"] = image_tag_mutability
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if repository_policy_text is not None:
            self._values["repository_policy_text"] = repository_policy_text
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.EncryptionConfigurationProperty]]:
        '''``AWS::ECR::Repository.EncryptionConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-encryptionconfiguration
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.EncryptionConfigurationProperty]], result)

    @builtins.property
    def image_scanning_configuration(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.ImageScanningConfigurationProperty]]:
        '''``AWS::ECR::Repository.ImageScanningConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagescanningconfiguration
        '''
        result = self._values.get("image_scanning_configuration")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.ImageScanningConfigurationProperty]], result)

    @builtins.property
    def image_tag_mutability(self) -> typing.Optional[builtins.str]:
        '''``AWS::ECR::Repository.ImageTagMutability``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-imagetagmutability
        '''
        result = self._values.get("image_tag_mutability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_policy(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.LifecyclePolicyProperty]]:
        '''``AWS::ECR::Repository.LifecyclePolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-lifecyclepolicy
        '''
        result = self._values.get("lifecycle_policy")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnRepository.LifecyclePolicyProperty]], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::ECR::Repository.RepositoryName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositoryname
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_policy_text(self) -> typing.Any:
        '''``AWS::ECR::Repository.RepositoryPolicyText``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-repositorypolicytext
        '''
        result = self._values.get("repository_policy_text")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::ECR::Repository.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecr-repository.html#cfn-ecr-repository-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-ecr.IRepository")
class IRepository(aws_cdk.core.IResource, typing_extensions.Protocol):
    '''Represents an ECR repository.'''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        '''The ARN of the repository.

        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the repository.

        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        '''The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        '''Add a policy statement to the repository's resource policy.

        :param statement: -
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -
        '''
        ...

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        '''Grant the given identity permissions to pull images in this repository.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        ...

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(
        self,
        id: builtins.str,
        *,
        image_tag: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        ...

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(
        self,
        id: builtins.str,
        *,
        image_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines an AWS CloudWatch event rule that can trigger a target when the image scan is completed.

        :param id: The id of the rule.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        ...

    @jsii.member(jsii_name="repositoryUriForDigest")
    def repository_uri_for_digest(
        self,
        digest: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Returns the URI of the repository for a certain tag. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[@DIGEST]

        :param digest: Image digest to use (tools usually default to the image with the "latest" tag if omitted).
        '''
        ...

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(
        self,
        tag: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Returns the URI of the repository for a certain tag. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Image tag to use (tools usually default to "latest" if omitted).
        '''
        ...


class _IRepositoryProxy(
    jsii.proxy_for(aws_cdk.core.IResource) # type: ignore[misc]
):
    '''Represents an ECR repository.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ecr.IRepository"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        '''The ARN of the repository.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the repository.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        '''The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryUri"))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        '''Add a policy statement to the repository's resource policy.

        :param statement: -
        '''
        return typing.cast(aws_cdk.aws_iam.AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -
        '''
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        '''Grant the given identity permissions to pull images in this repository.

        :param grantee: -
        '''
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantPull", [grantee]))

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -
        '''
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantPullPush", [grantee]))

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onCloudTrailEvent", [id, options]))

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(
        self,
        id: builtins.str,
        *,
        image_tag: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        options = OnCloudTrailImagePushedOptions(
            image_tag=image_tag,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onCloudTrailImagePushed", [id, options]))

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onEvent", [id, options]))

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(
        self,
        id: builtins.str,
        *,
        image_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines an AWS CloudWatch event rule that can trigger a target when the image scan is completed.

        :param id: The id of the rule.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        options = OnImageScanCompletedOptions(
            image_tags=image_tags,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onImageScanCompleted", [id, options]))

    @jsii.member(jsii_name="repositoryUriForDigest")
    def repository_uri_for_digest(
        self,
        digest: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Returns the URI of the repository for a certain tag. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[@DIGEST]

        :param digest: Image digest to use (tools usually default to the image with the "latest" tag if omitted).
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "repositoryUriForDigest", [digest]))

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(
        self,
        tag: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Returns the URI of the repository for a certain tag. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Image tag to use (tools usually default to "latest" if omitted).
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "repositoryUriForTag", [tag]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRepository).__jsii_proxy_class__ = lambda : _IRepositoryProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.LifecycleRule",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "max_image_age": "maxImageAge",
        "max_image_count": "maxImageCount",
        "rule_priority": "rulePriority",
        "tag_prefix_list": "tagPrefixList",
        "tag_status": "tagStatus",
    },
)
class LifecycleRule:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        max_image_age: typing.Optional[aws_cdk.core.Duration] = None,
        max_image_count: typing.Optional[jsii.Number] = None,
        rule_priority: typing.Optional[jsii.Number] = None,
        tag_prefix_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_status: typing.Optional["TagStatus"] = None,
    ) -> None:
        '''An ECR life cycle rule.

        :param description: Describes the purpose of the rule. Default: No description
        :param max_image_age: The maximum age of images to retain. The value must represent a number of days. Specify exactly one of maxImageCount and maxImageAge.
        :param max_image_count: The maximum number of images to retain. Specify exactly one of maxImageCount and maxImageAge.
        :param rule_priority: Controls the order in which rules are evaluated (low to high). All rules must have a unique priority, where lower numbers have higher precedence. The first rule that matches is applied to an image. There can only be one rule with a tagStatus of Any, and it must have the highest rulePriority. All rules without a specified priority will have incrementing priorities automatically assigned to them, higher than any rules that DO have priorities. Default: Automatically assigned
        :param tag_prefix_list: Select images that have ALL the given prefixes in their tag. Only if tagStatus == TagStatus.Tagged
        :param tag_status: Select images based on tags. Only one rule is allowed to select untagged images, and it must have the highest rulePriority. Default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if max_image_age is not None:
            self._values["max_image_age"] = max_image_age
        if max_image_count is not None:
            self._values["max_image_count"] = max_image_count
        if rule_priority is not None:
            self._values["rule_priority"] = rule_priority
        if tag_prefix_list is not None:
            self._values["tag_prefix_list"] = tag_prefix_list
        if tag_status is not None:
            self._values["tag_status"] = tag_status

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Describes the purpose of the rule.

        :default: No description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_image_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''The maximum age of images to retain. The value must represent a number of days.

        Specify exactly one of maxImageCount and maxImageAge.
        '''
        result = self._values.get("max_image_age")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def max_image_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of images to retain.

        Specify exactly one of maxImageCount and maxImageAge.
        '''
        result = self._values.get("max_image_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rule_priority(self) -> typing.Optional[jsii.Number]:
        '''Controls the order in which rules are evaluated (low to high).

        All rules must have a unique priority, where lower numbers have
        higher precedence. The first rule that matches is applied to an image.

        There can only be one rule with a tagStatus of Any, and it must have
        the highest rulePriority.

        All rules without a specified priority will have incrementing priorities
        automatically assigned to them, higher than any rules that DO have priorities.

        :default: Automatically assigned
        '''
        result = self._values.get("rule_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tag_prefix_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Select images that have ALL the given prefixes in their tag.

        Only if tagStatus == TagStatus.Tagged
        '''
        result = self._values.get("tag_prefix_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_status(self) -> typing.Optional["TagStatus"]:
        '''Select images based on tags.

        Only one rule is allowed to select untagged images, and it must
        have the highest rulePriority.

        :default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise
        '''
        result = self._values.get("tag_status")
        return typing.cast(typing.Optional["TagStatus"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecycleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.OnCloudTrailImagePushedOptions",
    jsii_struct_bases=[aws_cdk.aws_events.OnEventOptions],
    name_mapping={
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "target": "target",
        "image_tag": "imageTag",
    },
)
class OnCloudTrailImagePushedOptions(aws_cdk.aws_events.OnEventOptions):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        image_tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Options for the onCloudTrailImagePushed method.

        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        '''
        if isinstance(event_pattern, dict):
            event_pattern = aws_cdk.aws_events.EventPattern(**event_pattern)
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if target is not None:
            self._values["target"] = target
        if image_tag is not None:
            self._values["image_tag"] = image_tag

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule's purpose.

        :default: - No description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_pattern(self) -> typing.Optional[aws_cdk.aws_events.EventPattern]:
        '''Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        '''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Optional[aws_cdk.aws_events.EventPattern], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[aws_cdk.aws_events.IRuleTarget]:
        '''The target to register for the event.

        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[aws_cdk.aws_events.IRuleTarget], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''Only watch changes to this image tag.

        :default: - Watch changes to all tags
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCloudTrailImagePushedOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.OnImageScanCompletedOptions",
    jsii_struct_bases=[aws_cdk.aws_events.OnEventOptions],
    name_mapping={
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "target": "target",
        "image_tags": "imageTags",
    },
)
class OnImageScanCompletedOptions(aws_cdk.aws_events.OnEventOptions):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
        image_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Options for the OnImageScanCompleted method.

        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        '''
        if isinstance(event_pattern, dict):
            event_pattern = aws_cdk.aws_events.EventPattern(**event_pattern)
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if target is not None:
            self._values["target"] = target
        if image_tags is not None:
            self._values["image_tags"] = image_tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule's purpose.

        :default: - No description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_pattern(self) -> typing.Optional[aws_cdk.aws_events.EventPattern]:
        '''Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        '''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Optional[aws_cdk.aws_events.EventPattern], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[aws_cdk.aws_events.IRuleTarget]:
        '''The target to register for the event.

        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[aws_cdk.aws_events.IRuleTarget], result)

    @builtins.property
    def image_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Only watch changes to the image tags spedified.

        Leave it undefined to watch the full repository.

        :default: - Watch the changes to the repository with all image tags
        '''
        result = self._values.get("image_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnImageScanCompletedOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PublicGalleryAuthorizationToken(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr.PublicGalleryAuthorizationToken",
):
    '''Authorization token to access the global public ECR Gallery via Docker CLI.

    :see: https://docs.aws.amazon.com/AmazonECR/latest/public/public-registries.html#public-registry-auth
    '''

    @jsii.member(jsii_name="grantRead") # type: ignore[misc]
    @builtins.classmethod
    def grant_read(cls, grantee: aws_cdk.aws_iam.IGrantable) -> None:
        '''Grant access to retrieve an authorization token.

        :param grantee: -
        '''
        return typing.cast(None, jsii.sinvoke(cls, "grantRead", [grantee]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.RepositoryAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "repository_arn": "repositoryArn",
        "repository_name": "repositoryName",
    },
)
class RepositoryAttributes:
    def __init__(
        self,
        *,
        repository_arn: builtins.str,
        repository_name: builtins.str,
    ) -> None:
        '''
        :param repository_arn: 
        :param repository_name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "repository_arn": repository_arn,
            "repository_name": repository_name,
        }

    @builtins.property
    def repository_arn(self) -> builtins.str:
        result = self._values.get("repository_arn")
        assert result is not None, "Required property 'repository_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRepository)
class RepositoryBase(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-ecr.RepositoryBase",
):
    '''Base class for ECR repository.

    Reused between imported repositories and owned repositories.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        props = aws_cdk.core.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addToResourcePolicy") # type: ignore[misc]
    @abc.abstractmethod
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        '''Add a policy statement to the repository's resource policy.

        :param statement: -
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
        *actions: builtins.str,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -
        '''
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        '''Grant the given identity permissions to use the images in this repository.

        :param grantee: -
        '''
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantPull", [grantee]))

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(
        self,
        grantee: aws_cdk.aws_iam.IGrantable,
    ) -> aws_cdk.aws_iam.Grant:
        '''Grant the given identity permissions to pull and push images to this repository.

        :param grantee: -
        '''
        return typing.cast(aws_cdk.aws_iam.Grant, jsii.invoke(self, "grantPullPush", [grantee]))

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onCloudTrailEvent", [id, options]))

    @jsii.member(jsii_name="onCloudTrailImagePushed")
    def on_cloud_trail_image_pushed(
        self,
        id: builtins.str,
        *,
        image_tag: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines an AWS CloudWatch event rule that can trigger a target when an image is pushed to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param image_tag: Only watch changes to this image tag. Default: - Watch changes to all tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        options = OnCloudTrailImagePushedOptions(
            image_tag=image_tag,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onCloudTrailImagePushed", [id, options]))

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        options = aws_cdk.aws_events.OnEventOptions(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onEvent", [id, options]))

    @jsii.member(jsii_name="onImageScanCompleted")
    def on_image_scan_completed(
        self,
        id: builtins.str,
        *,
        image_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[aws_cdk.aws_events.IRuleTarget] = None,
    ) -> aws_cdk.aws_events.Rule:
        '''Defines an AWS CloudWatch event rule that can trigger a target when an image scan is completed.

        :param id: The id of the rule.
        :param image_tags: Only watch changes to the image tags spedified. Leave it undefined to watch the full repository. Default: - Watch the changes to the repository with all image tags
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        '''
        options = OnImageScanCompletedOptions(
            image_tags=image_tags,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(aws_cdk.aws_events.Rule, jsii.invoke(self, "onImageScanCompleted", [id, options]))

    @jsii.member(jsii_name="repositoryUriForDigest")
    def repository_uri_for_digest(
        self,
        digest: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Returns the URL of the repository. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[@DIGEST]

        :param digest: Optional image digest.
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "repositoryUriForDigest", [digest]))

    @jsii.member(jsii_name="repositoryUriForTag")
    def repository_uri_for_tag(
        self,
        tag: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Returns the URL of the repository. Can be used in ``docker push/pull``.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY[:TAG]

        :param tag: Optional image tag.
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "repositoryUriForTag", [tag]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryArn")
    @abc.abstractmethod
    def repository_arn(self) -> builtins.str:
        '''The ARN of the repository.'''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryName")
    @abc.abstractmethod
    def repository_name(self) -> builtins.str:
        '''The name of the repository.'''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryUri")
    def repository_uri(self) -> builtins.str:
        '''The URI of this repository (represents the latest image):.

        ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPOSITORY
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryUri"))


class _RepositoryBaseProxy(
    RepositoryBase, jsii.proxy_for(aws_cdk.core.Resource) # type: ignore[misc]
):
    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        '''Add a policy statement to the repository's resource policy.

        :param statement: -
        '''
        return typing.cast(aws_cdk.aws_iam.AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        '''The ARN of the repository.'''
        return typing.cast(builtins.str, jsii.get(self, "repositoryArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the repository.'''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, RepositoryBase).__jsii_proxy_class__ = lambda : _RepositoryBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecr.RepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_scan_on_push": "imageScanOnPush",
        "image_tag_mutability": "imageTagMutability",
        "lifecycle_registry_id": "lifecycleRegistryId",
        "lifecycle_rules": "lifecycleRules",
        "removal_policy": "removalPolicy",
        "repository_name": "repositoryName",
    },
)
class RepositoryProps:
    def __init__(
        self,
        *,
        image_scan_on_push: typing.Optional[builtins.bool] = None,
        image_tag_mutability: typing.Optional["TagMutability"] = None,
        lifecycle_registry_id: typing.Optional[builtins.str] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[LifecycleRule]] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_scan_on_push: Enable the scan on push when creating the repository. Default: false
        :param image_tag_mutability: The tag mutability setting for the repository. If this parameter is omitted, the default setting of MUTABLE will be used which will allow image tags to be overwritten. Default: TagMutability.MUTABLE
        :param lifecycle_registry_id: The AWS account ID associated with the registry that contains the repository. Default: The default registry is assumed.
        :param lifecycle_rules: Life cycle rules to apply to this registry. Default: No life cycle rules
        :param removal_policy: Determine what happens to the repository when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param repository_name: Name for this repository. Default: Automatically generated name.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if image_scan_on_push is not None:
            self._values["image_scan_on_push"] = image_scan_on_push
        if image_tag_mutability is not None:
            self._values["image_tag_mutability"] = image_tag_mutability
        if lifecycle_registry_id is not None:
            self._values["lifecycle_registry_id"] = lifecycle_registry_id
        if lifecycle_rules is not None:
            self._values["lifecycle_rules"] = lifecycle_rules
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if repository_name is not None:
            self._values["repository_name"] = repository_name

    @builtins.property
    def image_scan_on_push(self) -> typing.Optional[builtins.bool]:
        '''Enable the scan on push when creating the repository.

        :default: false
        '''
        result = self._values.get("image_scan_on_push")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def image_tag_mutability(self) -> typing.Optional["TagMutability"]:
        '''The tag mutability setting for the repository.

        If this parameter is omitted, the default setting of MUTABLE will be used which will allow image tags to be overwritten.

        :default: TagMutability.MUTABLE
        '''
        result = self._values.get("image_tag_mutability")
        return typing.cast(typing.Optional["TagMutability"], result)

    @builtins.property
    def lifecycle_registry_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID associated with the registry that contains the repository.

        :default: The default registry is assumed.

        :see: https://docs.aws.amazon.com/AmazonECR/latest/APIReference/API_PutLifecyclePolicy.html
        '''
        result = self._values.get("lifecycle_registry_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_rules(self) -> typing.Optional[typing.List[LifecycleRule]]:
        '''Life cycle rules to apply to this registry.

        :default: No life cycle rules
        '''
        result = self._values.get("lifecycle_rules")
        return typing.cast(typing.Optional[typing.List[LifecycleRule]], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        '''Determine what happens to the repository when the resource/stack is deleted.

        :default: RemovalPolicy.Retain
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[aws_cdk.core.RemovalPolicy], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''Name for this repository.

        :default: Automatically generated name.
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-ecr.TagMutability")
class TagMutability(enum.Enum):
    '''The tag mutability setting for your repository.'''

    MUTABLE = "MUTABLE"
    '''allow image tags to be overwritten.'''
    IMMUTABLE = "IMMUTABLE"
    '''all image tags within the repository will be immutable which will prevent them from being overwritten.'''


@jsii.enum(jsii_type="@aws-cdk/aws-ecr.TagStatus")
class TagStatus(enum.Enum):
    '''Select images based on tags.'''

    ANY = "ANY"
    '''Rule applies to all images.'''
    TAGGED = "TAGGED"
    '''Rule applies to tagged images.'''
    UNTAGGED = "UNTAGGED"
    '''Rule applies to untagged images.'''


class Repository(
    RepositoryBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecr.Repository",
):
    '''Define an ECR repository.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        image_scan_on_push: typing.Optional[builtins.bool] = None,
        image_tag_mutability: typing.Optional[TagMutability] = None,
        lifecycle_registry_id: typing.Optional[builtins.str] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[LifecycleRule]] = None,
        removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image_scan_on_push: Enable the scan on push when creating the repository. Default: false
        :param image_tag_mutability: The tag mutability setting for the repository. If this parameter is omitted, the default setting of MUTABLE will be used which will allow image tags to be overwritten. Default: TagMutability.MUTABLE
        :param lifecycle_registry_id: The AWS account ID associated with the registry that contains the repository. Default: The default registry is assumed.
        :param lifecycle_rules: Life cycle rules to apply to this registry. Default: No life cycle rules
        :param removal_policy: Determine what happens to the repository when the resource/stack is deleted. Default: RemovalPolicy.Retain
        :param repository_name: Name for this repository. Default: Automatically generated name.
        '''
        props = RepositoryProps(
            image_scan_on_push=image_scan_on_push,
            image_tag_mutability=image_tag_mutability,
            lifecycle_registry_id=lifecycle_registry_id,
            lifecycle_rules=lifecycle_rules,
            removal_policy=removal_policy,
            repository_name=repository_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForLocalRepository") # type: ignore[misc]
    @builtins.classmethod
    def arn_for_local_repository(
        cls,
        repository_name: builtins.str,
        scope: constructs.IConstruct,
        account: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Returns an ECR ARN for a repository that resides in the same account/region as the current stack.

        :param repository_name: -
        :param scope: -
        :param account: -
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForLocalRepository", [repository_name, scope, account]))

    @jsii.member(jsii_name="fromRepositoryArn") # type: ignore[misc]
    @builtins.classmethod
    def from_repository_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        repository_arn: builtins.str,
    ) -> IRepository:
        '''
        :param scope: -
        :param id: -
        :param repository_arn: -
        '''
        return typing.cast(IRepository, jsii.sinvoke(cls, "fromRepositoryArn", [scope, id, repository_arn]))

    @jsii.member(jsii_name="fromRepositoryAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_repository_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        repository_arn: builtins.str,
        repository_name: builtins.str,
    ) -> IRepository:
        '''Import a repository.

        :param scope: -
        :param id: -
        :param repository_arn: 
        :param repository_name: 
        '''
        attrs = RepositoryAttributes(
            repository_arn=repository_arn, repository_name=repository_name
        )

        return typing.cast(IRepository, jsii.sinvoke(cls, "fromRepositoryAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromRepositoryName") # type: ignore[misc]
    @builtins.classmethod
    def from_repository_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        repository_name: builtins.str,
    ) -> IRepository:
        '''
        :param scope: -
        :param id: -
        :param repository_name: -
        '''
        return typing.cast(IRepository, jsii.sinvoke(cls, "fromRepositoryName", [scope, id, repository_name]))

    @jsii.member(jsii_name="addLifecycleRule")
    def add_lifecycle_rule(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        max_image_age: typing.Optional[aws_cdk.core.Duration] = None,
        max_image_count: typing.Optional[jsii.Number] = None,
        rule_priority: typing.Optional[jsii.Number] = None,
        tag_prefix_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_status: typing.Optional[TagStatus] = None,
    ) -> None:
        '''Add a life cycle rule to the repository.

        Life cycle rules automatically expire images from the repository that match
        certain conditions.

        :param description: Describes the purpose of the rule. Default: No description
        :param max_image_age: The maximum age of images to retain. The value must represent a number of days. Specify exactly one of maxImageCount and maxImageAge.
        :param max_image_count: The maximum number of images to retain. Specify exactly one of maxImageCount and maxImageAge.
        :param rule_priority: Controls the order in which rules are evaluated (low to high). All rules must have a unique priority, where lower numbers have higher precedence. The first rule that matches is applied to an image. There can only be one rule with a tagStatus of Any, and it must have the highest rulePriority. All rules without a specified priority will have incrementing priorities automatically assigned to them, higher than any rules that DO have priorities. Default: Automatically assigned
        :param tag_prefix_list: Select images that have ALL the given prefixes in their tag. Only if tagStatus == TagStatus.Tagged
        :param tag_status: Select images based on tags. Only one rule is allowed to select untagged images, and it must have the highest rulePriority. Default: TagStatus.Tagged if tagPrefixList is given, TagStatus.Any otherwise
        '''
        rule = LifecycleRule(
            description=description,
            max_image_age=max_image_age,
            max_image_count=max_image_count,
            rule_priority=rule_priority,
            tag_prefix_list=tag_prefix_list,
            tag_status=tag_status,
        )

        return typing.cast(None, jsii.invoke(self, "addLifecycleRule", [rule]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> aws_cdk.aws_iam.AddToResourcePolicyResult:
        '''Add a policy statement to the repository's resource policy.

        :param statement: -
        '''
        return typing.cast(aws_cdk.aws_iam.AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        '''The ARN of the repository.'''
        return typing.cast(builtins.str, jsii.get(self, "repositoryArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the repository.'''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))


__all__ = [
    "AuthorizationToken",
    "CfnPublicRepository",
    "CfnPublicRepositoryProps",
    "CfnRegistryPolicy",
    "CfnRegistryPolicyProps",
    "CfnReplicationConfiguration",
    "CfnReplicationConfigurationProps",
    "CfnRepository",
    "CfnRepositoryProps",
    "IRepository",
    "LifecycleRule",
    "OnCloudTrailImagePushedOptions",
    "OnImageScanCompletedOptions",
    "PublicGalleryAuthorizationToken",
    "Repository",
    "RepositoryAttributes",
    "RepositoryBase",
    "RepositoryProps",
    "TagMutability",
    "TagStatus",
]

publication.publish()
