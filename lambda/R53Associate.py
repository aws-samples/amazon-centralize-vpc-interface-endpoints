import os, boto3, json
import logging

logger = logging.getLogger("__name__")
logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
r53_client = boto3.client('route53')
sts_connection = boto3.client('sts')

def handler(event, context):
    logger.info("custom resource triggered by {} request type: {}".format(event.get('StackId'), event.get('RequestType')))
    logger.info("custom resource invoked with these properties: {}".format(event.get('ResourceProperties')))
    
    # Get the variables from the Custom Resource
    properties = event.get("ResourceProperties")
    vpc_id = properties.get("VPCID")
    phz_id = properties.get("HostedZoneID")
    account_id = properties.get("AccountID")
    RoleArn = properties.get("RoleARN")


    # Run the function depending on Request Type
    request_type = event['RequestType']
    if request_type == 'Create': return authenticate_and_associate_vpc_to_hosted_zone(vpc_id, phz_id, account_id, RoleArn)
    if request_type == 'Update': return authenticate_and_associate_vpc_to_hosted_zone(vpc_id, phz_id, account_id, RoleArn)
    if request_type == 'Delete': return disassociate_vpc_from_hosted_zone(vpc_id, phz_id)
    raise Exception("Invalid request type: %s" % request_type)

def authenticate_and_associate_vpc_to_hosted_zone(vpc_id, phz_id, account_id, RoleArn):
    # Authenticate the VPC to the PHZ
        try:
            # Assume a Role in Hub
            logger.info ("Assuming Role in Hub")
            acct_b = sts_connection.assume_role(
                RoleArn=RoleArn,
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
            response = assumed_r53_client.create_vpc_association_authorization(
                HostedZoneId= phz_id,
                VPC={
                    'VPCRegion': os.environ['AWS_REGION'],
                    'VPCId':  vpc_id
                }
            )
            logger.info("authorization is complete :\n {}".format(response))
        except Exception as ex:
            logger.error("Error authorizing %s to hosted zone %s : %s", vpc_id, phz_id, ex, exc_info=True)
            raise ex

        # Authorize the VPC to the PHZ
        try:
            logger.info("associating {} to hosted zone {} for account {}".format(vpc_id, phz_id, account_id))
            response = r53_client.associate_vpc_with_hosted_zone(
                HostedZoneId= phz_id,
                VPC={
                    'VPCRegion': os.environ['AWS_REGION'],
                    'VPCId':  vpc_id
                },
                Comment="VPC from {}".format(account_id)
            )
            logger.info("association is complete : \n {}".format(response))
        except Exception as ex:
            logger.error("Error associating %s to hosted zone %s : %s", vpc_id, phz_id, ex, exc_info=True)
            raise ex

def disassociate_vpc_from_hosted_zone(vpc_id, phz_id):
        try:
            logger.info("disassociation {} from hosted zone {}".format(vpc_id, phz_id))
            response = r53_client.disassociate_vpc_from_hosted_zone(
                HostedZoneId= phz_id,
                VPC={
                    'VPCRegion': os.environ['AWS_REGION'],
                    'VPCId':  vpc_id
                },
            )
            logger.info("disassociation is complete : \n {}".format(response))
        except Exception as ex:
            logger.error("Error disassociation %s to hosted zone %s : %s", vpc_id, phz_id, ex, exc_info=True)
            raise ex