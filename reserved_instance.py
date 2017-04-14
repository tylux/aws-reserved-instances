#!/usr/local/bin/python

import boto3

session = boto3.Session()

#connections
ri_conn = session.client('ec2')
ec2_conn = session.resource('ec2')

# Define ec2 instance units, https://aws.amazon.com/blogs/aws/new-instance-size-flexibility-for-ec2-reserved-instances/
instance_Types = {
    "t1.micro": 1,
    "t2.micro": 1,
    "t2.small": 2,
    "t2.medium": 4,
    "t2.large": 8,
    "t2.xlarge": 16,
    "t2.2xlarge": 32,
    "m1.small": 2,
    "m3.medium": 1,
    "m3.large": 2,
    "m3.xlarge": 4,
    "m3.2xlarge": 8,
    "m4.large": 1,
    "m4.xlarge": 2,
    "m4.2xlarge": 4,
    "m4.4xlarge": 8,
    "m4.10xlarge": 16,
    "m4.16xlatge": 32,
    "c3.large": 1,
    "c3.xlarge": 2,
    "c3.2xlarge": 4,
    "c3.4xlarge": 8,
    "c3.8xlarge": 16,
    "c4.large": 1,
    "c4.xlarge": 2,
    "c4.2xlarge": 4,
    "c4.4xlarge": 8,
    "c4.8xlarge": 16,
    "r3.large": 1,
    "r3.xlarge": 2,
    "r3.2xlarge": 4,
    "r3.4xlarge": 8,
    "r3.8xlarge": 16,
    "r4.large": 1,
    "r4.xlarge": 2,
    "r4.2xlarge": 4,
    "r4.4xlarge": 8,
    "r4.8xlarge": 16,
    "r4.16xlarge": 32,
    "i3.large": 1,
    "i3.xlarge": 2,
    "i3.2xlarge": 4,
    "i3.4xlarge": 8,
    "i3.8xlarge": 16,
    "i3.16xlarge": 32
}

############################
#
#
# Gather Reserved Instance information and convert to RI units and add to ri_count dictionary
#
#
###########################

# Reserved Instance Dictionary
ri_count = {}
# Get all reserved instances and look up the number of RI units and add ot the ri_count dictionary
reserved_instances = ri_conn.describe_reserved_instances(Filters=[{'Name': 'state', 'Values': ['active']}])['ReservedInstances']
for p in reserved_instances:
    types = p['InstanceType'][:2]
    number = (instance_Types.get(p['InstanceType']) * p['InstanceCount'])
    if types in ri_count:
        ri_count[types] += number
    else:
        ri_count[types] = number

############################
#
#
# Gather Running Instance Information, excluding Windoze....
#
#
############################

# Running Instance Dictionary
ec2_count = {}

instances = ec2_conn.instances.filter(Filters=[{'Name': 'instance-state-name','Values': ['running']}])
for i in instances:
    # Ignore Windows Instances for now....
    if i.platform is None:
        types = i.instance_type[:2]
        number = (instance_Types.get(i.instance_type))
        if types in ec2_count:
            try:
                ec2_count[types] += number
            except:
                print("Instance %s is not defined in instance_Types dictionary, edit script if you need and add it!") % i.instance_type
        else:
            ec2_count[types] = number

############################
#
#
# Print the things
#
#
############################

# Print Reserve Instance info
for k, v in ec2_count.items():
    try:
        print "%s Reserved Instance Coverage is: %.2f%% \t RI Count: %s \t EC2 Units: %s" % (k, float(ri_count.get(k) / float(v)) * 100, float(ri_count.get(k)), float(v))
    except:
        pass

# Total RI Coverage
ri = sum(ri_count.values())
ec2 = sum(ec2_count.values())

print "Total: %.2f%% \n" % (float(ri) / float(ec2) * 100)
# Print total....
# Print Instances that don't have any RIs
for k in ec2_count.keys():
    if not k in ri_count:
        print "Reserved Instances not purchased for Type: %s Units: %s " % (k, ec2_count[k])

