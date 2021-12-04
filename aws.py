import requests
import boto3
import sys
import ipaddress

aws_access_key = ''
aws_secret_key = ''
region = 'us-east-2'
ipAddress = '172.16.90.43'



def awsInstanceReturnNic(ipAddress):
    ec2 = boto3.client('ec2', 
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_key,
    region_name = region)
    response = ec2.describe_instances()
    # Iterate through all the instances
    for x in range(0,len(response['Reservations'])):
        for y in range(0,len(response['Reservations'][x]['Instances'])):
            # Iterate through all Interfaces on an instance
            for z in range(0,len(response['Reservations'][x]['Instances'][y]['NetworkInterfaces'])):
                # See if Interface Private IP matches the queried ipAddress
                if ipAddress == response['Reservations'][x]['Instances'][y]['NetworkInterfaces'][z]['PrivateIpAddress']:
                    # Return NIC ID
                    return(response['Reservations'][x]['Instances'][y]['NetworkInterfaces'][z]['NetworkInterfaceId'])
                else:
                    continue


def awsInstanceReturnSg(ipAddress):
    # Create empty list
    sgList = []
    # Setup AWS connection
    ec2 = boto3.client('ec2', 
    aws_access_key_id = aws_access_key,
    aws_secret_access_key = aws_secret_key,
    region_name = region)
    # Grab all instances
    response = ec2.describe_instances()
    # Iterate through all the instances
    for x in range(0,len(response['Reservations'])):
        for y in range(0,len(response['Reservations'][x]['Instances'])):
            # Iterate through all Interfaces on an instance
            for z in range(0,len(response['Reservations'][x]['Instances'][y]['NetworkInterfaces'])):
                # See if Interface Private IP matches the queried ipAddress
                if ipAddress == response['Reservations'][x]['Instances'][y]['NetworkInterfaces'][z]['PrivateIpAddress']:
                    # Append associated SG ID to List
                    for a in range(0,len(response['Reservations'][x]['Instances'][y]['NetworkInterfaces'][z]['Groups'])):
                        sgList.append(response['Reservations'][x]['Instances'][y]['NetworkInterfaces'][z]['Groups'][a]['GroupId'])
                else:
                    continue
    return(sgList)



def awsSgInboundRules(sgList):
    # Create new list
    sgList = [sgList]
    inboundRuleList = []
    # AWS setup
    ec2 = boto3.resource('ec2',
        aws_access_key_id = aws_access_key,
        aws_secret_access_key = aws_secret_key,
        region_name = region)
    # Iterate through security group list
    for x in range(0,len(sgList)):
        security_group = ec2.SecurityGroup(sgList[x])
        # Add each rule to list
        for y in range(0,len(security_group.ip_permissions)):
            #print(security_group.ip_permissions[y])
            inboundRuleList.append(security_group.ip_permissions[y])
    # Return List
    return(inboundRuleList)


def awsIpAddressParser(ipAddress, cidr):
    if ipaddress.ip_address(ipAddress) in ipaddress.ip_network(cidr):
        return(True)
    else:
        return(False)


def awsPortParser(fromPort, toPort, requestPort):
    if requestPort in range(fromPort, toPort) or requestPort == fromPort:
        return(True)
    else:
        return(False)


if __name__ == '__main__':
    ipAddress = ipAddress
    srcIpAddress = '192.168.1.1'
    requestPort = 443
    sgList = awsInstanceReturnSg(ipAddress)
    for z in range(0,len(sgList)):
        inboundRules = awsSgInboundRules(sgList[z])
        for x in range(0,len(inboundRules)):
            for y in range(0,len(inboundRules[x]['IpRanges'])):
                parserReturnValue = awsIpAddressParser(srcIpAddress, inboundRules[x]['IpRanges'][y]['CidrIp'])
                #print(parserReturnValue)
                if parserReturnValue == True:
                    #print(inboundRules[x]['FromPort'])
                    #print(inboundRules[x]['ToPort'])
                    #print(requestPort)
                    portParser = awsPortParser(inboundRules[x]['FromPort'], inboundRules[x]['ToPort'], requestPort)
                    #print(portParser)
                    if portParser == True:
                        print('Matching Rule')
                        print(sgList[z])
                        print(inboundRules[x])
                    else:
                        print('No matching Port')
                else:
                    ('No mwatching Source IP')


