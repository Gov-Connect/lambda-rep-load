# AWS Lambda Augment-Representatives  
  
## Set up AWS EC2 instance (for replicating lambda environment)  
  
### Create EC2 Instance on AWS Console  
[Set up key pairs and security group]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html  
[Ensure IAM role has access to S3]: https://aws.amazon.com/premiumsupport/knowledge-center/ec2-instance-access-s3-bucket/  
[Launch the instance and connect]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html  
[Connect to instance through S3]: https://aws.amazon.com/premiumsupport/knowledge-center/ec2-instance-access-s3-bucket/  
  
### Set up env on EC2  
[Install Python 3.X (don't need final steps of installing EB CLI)]: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-linux.html  
[Set up virtual environment]: https://coffieldweb.com/weblog/2019/09/03/install-python-3-pip-3-and-virtualenv-amazon-linux-2/  
#### install git:  
`sudo yum install git -y`  
[git user name and email]: https://docs.github.com/en/github/getting-started-with-github/set-up-git  
[git token generation (for HTTPS)]: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token  
  
#### Install libraries and zip project to deploy in Lambda  
install two libraries (boto3 and pyyaml; installing all packages in 'lib'):  
`pip install pyyaml boto3  --upgrade --target /home/ec2-user/augment-reps/lib/python3.8/site-packages`  
navigate to virtual environment packages folder:  
`cd ../augment-reps/lib/python3.8/site-packages`  
zip contents of all packages and place zip file in project folder:  
`zip -r  ../../../../augment-representatives/augment-representatives.zip .`  
navigate back to project folder:  
 `cd ../../../../augment-representatives/`  
add script (and any other files, like keys) to zip file:  
 `zip -g augment-representatives.zip dailyRepLoad.py keys.yml`  
copy zip file to S3 to be used in AWS lambda:  
 `aws s3 cp augment-representatives.zip s3://gov-connect`  


### AWS Lambda set up  
  
#### Add lambda-policy.json  
```
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "Stmt1508266078275",
        "Action": [
          "logs:PutLogEvents",
          "logs:CreateLogGroup",
          "logs:CreateLogStream"
        ],
        "Effect": "Allow",
        "Resource": "*"
      }
    ]
  }
```  
#### Add trust-relationship.json  
```
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
```   
#### Create new lambda role (":wq" to quit vi)  
`aws iam create-role --role-name quotes-lambda-role --assume-role-policy-document file://trust-relationship.json`  
#### Create new lambda policy  
`aws iam create-policy --policy-name rep-augment-lambda-policy --policy-document file://lambda-policy.json`  
#### Attach Role Policy  
`aws iam attach-role-policy --policy-arn arn:aws:iam::350084813541:policy/rep-augment-lambda-policy  --role-name rep-augment-lambda-role`  
#### Delete the policy documents  
`rm -rf trust-relationship.json lambda-policy.json` 