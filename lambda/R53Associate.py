## Code Taken from https://aws.amazon.com/blogs/networking-and-content-delivery/automating-dns-infrastructure-using-route-53-resolver-endpoints/        

import os, boto3, json
import logging
import cfnresponse

logger = logging.getLogger("__name__")
logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
r53_client = boto3.client('route53')

def parameters(vpc_id, phz_id):
    return dict(
        HostedZoneId=phz_id,
        VPC={
            'VPCRegion': os.environ['AWS_REGION'],
            'VPCId': vpc_id
        }
    )

def associate_vpc_to_hosted_zone(vpc_ids, phz_id):
    for vpc_id in vpc_ids:
        try:
            logger.info("associating {} to hosted zone {}".format(vpc_id, phz_id))
            response = r53_client.associate_vpc_with_hosted_zone(**dict(parameters(vpc_id, phz_id)))
            logger.info("association is complete : \n {}".format(response))
        except Exception as ex:
            logger.error("Error associating %s to hosted zone %s : %s", vpc_id, phz_id, ex, exc_info=True)

def authorize_vpc_to_hosted_zone(vpc_ids, phz_id):
    for vpc_id in vpc_ids:
        try:
            # Assume a Role in Hub
            logger.info ("Assuming Role in Hub")
            sts_connection = boto3.client('sts')
            acct_b = sts_connection.assume_role(
                RoleArn="arn:aws:iam::222222222222:role/role-on-source-account",
                RoleSessionName="cross_acct_lambda"
            )
            
            ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
            SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
            SESSION_TOKEN = acct_b['Credentials']['SessionToken']

        # create service client using the assumed role credentials
            assumed_r53_client = boto3.client(
                'route53',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                aws_session_token=SESSION_TOKEN,
            )

            logger.info("authorizing {} to hosted zone {}".format(vpc_id, phz_id))
            response = assumed_r53_client.create_vpc_association_authorization(**dict(parameters(vpc_id, phz_id)))
            logger.info("authorization is complete :\n {}".format(response))
        except Exception as ex:
            logger.error("Error authorizing %s to hosted zone %s : %s", vpc_id, phz_id, ex, exc_info=True)

def disassociate_vpc_from_hosted_zone(vpc_ids, phz_id):
    for vpc_id in vpc_ids:
        try:
            logger.info("disassociation {} to hosted zone {}".format(vpc_id, phz_id))
            response = r53_client.disassociate_vpc_from_hosted_zone(**dict(parameters(vpc_id, phz_id)))
            logger.info("disassociation is complete :\n {}".format(response))
        except Exception as ex:
            logger.error("Error disassociation %s to hosted zone %s : %s", vpc_id, phz_id, ex, exc_info=True)

def deauthorize_vpc_to_hosted_zone(vpc_ids, phz_id):
    for vpc_id in vpc_ids:
        try:
            logger.info("delete authorization {} to hosted zone {}".format(vpc_id, phz_id))
            response = r53_client.delete_vpc_association_authorization(**dict(parameters(vpc_id, phz_id)))
            logger.info("delete authorization is complete:\n {}".format(response))
        except Exception as ex:
            logger.error("Error deleting authorization %s to hosted zone %s : %s", vpc_id, phz_id, ex,
                        exc_info=True)

def perform_action(action, vpc_ids, phz_id):
    if action == 'ASSOCIATE':
        associate_vpc_to_hosted_zone(vpc_ids, phz_id)
    elif action == 'AUTHORIZE':
        authorize_vpc_to_hosted_zone(vpc_ids, phz_id)
    elif action == 'DEAUTHORIZE':
        deauthorize_vpc_to_hosted_zone(vpc_ids, phz_id)
    elif action == 'DISASSOCIATE':
        disassociate_vpc_from_hosted_zone(vpc_ids, phz_id)

def handler(event, context):
    try:
        logger.info("custom resource triggered by {} request type: {}".format(event.get('StackId'), event.get('RequestType')))
        logger.info("custom resource invoked with these properties: {}".format(event.get('ResourceProperties')))
        properties = event.get("ResourceProperties")
        vpc_ids = properties.get("VPCID")
        phz_id = properties.get("HostedZoneID")
        event_type = event.get('RequestType')
        action = properties.get("Action")
        if event_type == 'Create' or event_type == 'Update':
            perform_action(action, vpc_ids, phz_id)
        elif event_type == 'Delete':
            perform_action(action, vpc_ids, phz_id)
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, phz_id)
    except Exception as ex:
        logger.error("Error performing actions: %s", ex, exc_info=True)
        if 'PhysicalResourceId' in event:
            cfnresponse.send(event, context, cfnresponse.FAILED, {}, event.get("PhysicalResourceId"))
        else:
            cfnresponse.send(event, context, cfnresponse.FAILED, {})
