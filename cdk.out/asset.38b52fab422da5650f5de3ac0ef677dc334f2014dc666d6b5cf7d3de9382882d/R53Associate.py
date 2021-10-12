import os, boto3, json
import logging

logger = logging.getLogger("__name__")
logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
r53_client = boto3.client("route53")

logger = logging.getLogger("__name__")
logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
r53_client = boto3.client("route53")


def handler(event, context):
    logger.info(
        "custom resource triggered by {} request type: {}".format(event.get("StackId"), event.get("RequestType"))
    )
    logger.info("custom resource invoked with these properties: {}".format(event.get("ResourceProperties")))

    # Get the variables from the Custom Resource
    properties = event.get("ResourceProperties")
    vpc_id = properties.get("VPCID")
    phz_id = properties.get("HostedZoneID")
    account_id = properties.get("AccountID")

    # Run the function depending on Request Type
    request_type = event["RequestType"]
    if request_type == "Create":
        return associate_vpc_to_hosted_zone(vpc_id, phz_id, account_id)
    if request_type == "Update":
        return associate_vpc_to_hosted_zone(vpc_id, phz_id, account_id)
    if request_type == "Delete":
        return disassociate_vpc_from_hosted_zone(vpc_id, phz_id)
    raise Exception("Invalid request type: %s" % request_type)


def parameters(vpc_id, phz_id):
    return dict(HostedZoneId=phz_id, VPC={"VPCRegion": os.environ["AWS_REGION"], "VPCId": vpc_id})


def associate_vpc_to_hosted_zone(vpc_id, phz_id, account_id):
    try:
        logger.info("associating {} to hosted zone {} for account {}".format(vpc_id, phz_id, account_id))
        response = r53_client.associate_vpc_with_hosted_zone(
            HostedZoneId=phz_id,
            VPC={"VPCRegion": os.environ["AWS_REGION"], "VPCId": vpc_id},
            Comment="VPC from {}".format(account_id),
        )
        logger.info("association is complete : \n {}".format(response))
    except Exception as ex:
        logger.error("Error associating %s to hosted zone %s : %s", vpc_id, phz_id, ex, exc_info=True)


def disassociate_vpc_from_hosted_zone(vpc_id, phz_id):
    try:
        logger.info("disassociation {} from hosted zone {}".format(vpc_id, phz_id))
        response = r53_client.disassociate_vpc_from_hosted_zone(
            HostedZoneId=phz_id,
            VPC={"VPCRegion": os.environ["AWS_REGION"], "VPCId": vpc_id},
        )
        logger.info("disassociation is complete : \n {}".format(response))
    except Exception as ex:
        logger.error("Error disassociation %s to hosted zone %s : %s", vpc_id, phz_id, ex, exc_info=True)
