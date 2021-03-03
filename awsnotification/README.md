# Setup AWS Notification

#### Step-1 Create SNS Topic and Subcription

* Go to SNS and Create standard topic with name restaurants_notify.

* Create subcription with protocal Email and slack email address.

#### Step-2 Add Lambda S3 trigger

* Go to AWS lambda service.

* Add trigger configuration with,
  * Bucket name
  * Event type: All object create events
  * prefix: directory path
  * suffix: snapshot file name

* Acknowledge and Click Add.

#### Step-3 Notify SNS Topic

* Go to Lambda Python source notify message to SNS Topic e.g.
```
import boto3
sns_client = boto3.client("sns", region_name="us-west-2")
response = sns.publish(
    TargetArn="arn:aws:sns:us-west-2:585684425594:restaurants_notify",
    Subject=("[Top Restaurants] Notification"),
    Message=("Here is top 10 restaurants.....")
)
print(response)
```


![AWS](https://raw.githubusercontent.com/venkatprasad33/govtechassessment/main/awsnotification/aws_workflow.png)