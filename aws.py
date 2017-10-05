n[1]:

import boto3
#create vpc
ec2 = boto3.resource(service_name='ec2') 
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
#Internet gateway
IG = ec2.create_internet_gateway()
#print(IG)
#Attach IG to VPC
response = IG.attach_to_vpc(DryRun=False,VpcId=vpc.id)
print(response)
#Create rout table 
RT = vpc.create_route_table()
#attch route to IG
route_ig_ipv4 = RT.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=IG.internet_gateway_id)

#Create public subnet 
subnet = ec2.create_subnet(VpcId = vpc.id, CidrBlock= '10.0.0.0/25')
#associate Route table with subnet 
RT.associate_with_subnet(SubnetId=subnet.id)


#steps for EC2 instance creation 
#.1keypair 
key_pair = ec2.create_key_pair(KeyName='TestKey')
KeyPairOut = str(key_pair.key_material)
#copy/download key pair to local system
outfile = open('TestKey.pem','w')
outfile.write(KeyPairOut)

#create instance 
firstInstance1 = subnet.create_instances(
    ImageId='ami-327f5352', 
    MinCount=1, 
    MaxCount=1,
    KeyName="TestKey",
    InstanceType="t2.micro")


# In[ ]:
