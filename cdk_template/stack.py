import os
from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
    aws_secretsmanager as secretsmanager,
    SecretValue,
    Stack,
    CfnParameter,
    CfnOutput,
    Fn
)


class CdkTemplateStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Set the backup name 
        if "BACKUP_NAME" in os.environ.keys():
            backup_name = os.environ["BACKUP_NAME"]
        else:
           print("ERROR: The environment variable 'BACKUP_NAME' is missing - aborting")
           raise Exception("The environment variable BACKUP_NAME is missing")

         # Set up a bucket
         # Currently, cfnBucket is used (instead of the esier "bucket", to support object-lock
         # Set up a bucket, w/encription, versioning, no public access and object lock
        object_lock_configuration_property = s3.CfnBucket.ObjectLockConfigurationProperty(
            object_lock_enabled="Enabled",
            rule=s3.CfnBucket.ObjectLockRuleProperty(
                default_retention=s3.CfnBucket.DefaultRetentionProperty( days=90, mode="GOVERNANCE")
            )
        )
                
        bucket_encryption=s3.CfnBucket.BucketEncryptionProperty(
           server_side_encryption_configuration=[
                s3.CfnBucket.ServerSideEncryptionRuleProperty(
                     server_side_encryption_by_default=s3.CfnBucket.ServerSideEncryptionByDefaultProperty(
                          sse_algorithm="AES256"
                     )
                )
           ]
        )
        
        public_access_block_configuration_property = s3.CfnBucket.PublicAccessBlockConfigurationProperty(
            block_public_acls=True,
            block_public_policy=True,
            ignore_public_acls=True,
            restrict_public_buckets=True
        )
        
        
        bucket = s3.CfnBucket(
            self, "bucket", bucket_name=backup_name +"-backup-bucket",
            bucket_encryption=bucket_encryption,
            versioning_configuration = {"status": "Enabled"},
            object_lock_configuration = object_lock_configuration_property,
            object_lock_enabled = True,
            public_access_block_configuration = public_access_block_configuration_property
        ) 

        #  Evreything: "s3:*"
        allowed_s3_actions = []
        allowed_s3_actions.append("s3:Abort*")
        allowed_s3_actions.append("s3:DeleteObject*")
        allowed_s3_actions.append("s3:GetBucket*")
        allowed_s3_actions.append("s3:GetObject*")
        allowed_s3_actions.append("s3:List*")
        allowed_s3_actions.append("s3:PutObject")
        allowed_s3_actions.append("s3:PutObjectLegalHold")
        allowed_s3_actions.append("s3:PutObjectRetention")
        allowed_s3_actions.append("s3:PutObjectTagging")
        allowed_s3_actions.append("s3:PutObjectVersionTagging")

        # Create an IAM user and associated access key
        iam_user = iam.User(self, backup_name +"Backupbackup_name")
        access_key = iam.AccessKey(self, "AccessKey", user=iam_user)
        secret = SecretValue.unsafe_unwrap(access_key.secret_access_key)


        # Create IAM policy and attach to user
        policyStatmentFullRightsBucket = iam.PolicyStatement(
                                         actions=allowed_s3_actions,
                                         resources=[bucket.attr_arn, bucket.attr_arn + "\*" ],
                                         )
        policyFullRightsBucke = iam.Policy(self, "bucket-full-rights-policy", 
                                          statements=[policyStatmentFullRightsBucket],
                                          users=[iam_user]
                                          )
        
      
        # Define stack output
        CfnOutput(self, 'bucketArn', value=bucket.attr_arn)
        CfnOutput(self, 'userName', value=iam_user.user_name)
        CfnOutput(self, 'userAccessKey', value=access_key.access_key_id)
        CfnOutput(self, 'userSecretAccessKey', value=secret)
        
