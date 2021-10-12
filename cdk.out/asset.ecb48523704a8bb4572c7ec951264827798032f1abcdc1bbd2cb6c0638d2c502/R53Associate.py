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
    properties = event.get("ResourceProperties")
    vpc_ids = properties.get("VPCID")
    phz_id = properties.get("HostedZoneID")
    request_type = event["RequestType"]
    if request_type == "Create":
        return associate_vpc_to_hosted_zone(vpc_ids, phz_id)
    if request_type == "Update":
        return associate_vpc_to_hosted_zone(vpc_ids, phz_id)
    if request_type == "Delete":
        return disassociate_vpc_from_hosted_zone(vpc_ids, phz_id)
    raise Exception("Invalid request type: %s" % request_type)


def associate_vpc_to_hosted_zone(vpc_ids, phz_id):
    for vpc_id in vpc_ids:
        try:
            logger.info("associating {} to hosted zone {}".format(vpc_id, phz_id))
            response = r53_client.associate_vpc_with_hosted_zone(**dict(parameters(vpc_id, phz_id)))
            logger.info("association is complete : \n {}".format(response))
        except Exception as ex:
            logger.error("Error associating %s to hosted zone %s : %s", vpc_id, phz_id, ex, exc_info=True)


def disassociate_vpc_from_hosted_zone(vpc_ids, phz_id):
    for vpc_id in vpc_ids:
        try:
            logger.info("disassociation {} to hosted zone {}".format(vpc_id, phz_id))
            response = r53_client.disassociate_vpc_from_hosted_zone(**dict(parameters(vpc_id, phz_id)))
            logger.info("disassociation is complete :\n {}".format(response))
        except Exception as ex:
            logger.error("Error disassociation %s to hosted zone %s : %s", vpc_id, phz_id, ex, exc_info=True)
