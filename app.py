#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from pro_serve_apg_centralised_vpc_endpoints.pro_serve_apg_centralised_vpc_endpoints_stack import ProServeApgCentralisedVpcEndpointsHubStack, ProServeApgCentralisedVpcEndpointsSpokeStack


app = core.App()

services =  ["ssm"]

hub_env = core.Environment()
spoke_env = core.Environment()


ProServeApgCentralisedVpcEndpointsHubStack(app, "ProServeApgCentralisedVpcEndpointsHubStack",    services=services, env=hub_env)
ProServeApgCentralisedVpcEndpointsSpokeStack(app, "ProServeApgCentralisedVpcEndpointsSpokeStack",services=services,  env=spoke_env  )

app.synth()
