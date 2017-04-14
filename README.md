# aws-reserved-instances

An attempt to create a report for AWS reserved instances based on the new Instance Size Flexibility for EC2 instances. https://aws.amazon.com/blogs/aws/new-instance-size-flexibility-for-ec2-reserved-instances/

This script attempts to assign a value to each instance type and calculate how many can fit into your reserved instances. 

Example: 2 t2.small ec2 instances can be covered by a single t2.medium reserved instance now.

Requires boto3 to be installed and aws cli tools be configured


#### Example Output:
```
r4 Reserved Instance Coverage is: 25.00%      RI Count: 2.0      EC2 Units: 8.0
r3 Reserved Instance Coverage is: 38.46%      RI Count: 10.0     EC2 Units: 26.0
t2 Reserved Instance Coverage is: 140.07%      RI Count: 152.0      EC2 Units: 108.0
Total RI Percentage: 107.08%

Reserved Instances not purchased for Type: i3 Units: 14
Reserved Instances not purchased for Type: c3 Units: 9
```
