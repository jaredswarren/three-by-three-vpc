from crhelper import CfnResource
import json
import boto3

helper = CfnResource()

fwclient = boto3.client('network-firewall')
ec2client = boto3.client('ec2')

@helper.create
@helper.update
def sum_2_numbers(event, _):
    routes = event['ResourceProperties']['Routes']
    print(routes)

    fw = fwclient.describe_firewall(FirewallName='NetworkFirewall')
    fwstate = fw['FirewallStatus']['SyncStates']
    gatewayId=event['ResourceProperties']['GatewayId']
    print(json.dumps(fwstate,indent=2))
    routeTable = ec2client.create_route_table(
        VpcId=event['ResourceProperties']['VpcId'],
        TagSpecifications=[ {
            'ResourceType': 'route-table',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '3x3-igw'
                }    
            ]
        }
        ]
    )
    routeTableId = routeTable['RouteTable']['RouteTableId']
    for route in routes:
        az = route['AvailabilityZone']
        protectedSubnet = route['ProtectedSubnet']
        vpce = fwstate[az]['Attachment']['EndpointId']
        print("VPCE: "+vpce)
        ec2subnet = ec2client.describe_subnets(
            Filters=[
                {
                    'Name': 'subnet-id',
                    'Values': [protectedSubnet]
                }
                ]
            )
        protectedCidrBlock = ec2subnet['Subnets'][0]['CidrBlock']
        print("Protected Cidr Block: "+protectedCidrBlock)
        ec2client.create_route(
            RouteTableId=routeTableId,
            DestinationCidrBlock=protectedCidrBlock,
            VpcEndpointId=vpce,
        )
    print("Associating....")
    ec2client.associate_route_table(
        RouteTableId=routeTableId,
        GatewayId=gatewayId
        )
    print("Associated...")

@helper.delete
def no_op(_, __):
    pass

def handler(event, context):
    print(event)
    helper(event, context)