## Centralize access using VPC interface endpoints to access AWS services across multiple VPCs

Security and cost are always a top priority for AWS customers when designing their network. Amazon Virtual Private Cloud (Amazon VPC),  and it’s related networking components, offer many tools for implementing network connectivity. One such tool is VPC endpoints. Powered by AWS PrivateLink, VPC endpoints are private connections between your VPC and another AWS service without sending traffic over the internet, through a NAT instance, a VPN connection, or AWS Direct Connect. In this blog post, I present hub and spoke design where all the spoke VPCs use an interface VPC endpoint provisioned inside the hub (shared services) VPC. This architecture may help reduce the cost and maintenance for multiple interface VPC endpoints across different VPCs.

This code has been created to compliment the blog https://aws.amazon.com/blogs/networking-and-content-delivery/centralize-access-using-vpc-interface-endpoints/

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

