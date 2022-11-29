# Easy Cloud Backup

This repository automate setting up an AWS-based storage for backup.

Specifically, it contains an AWS-CDK stack for setting up an S3 bucket, with the associated dedicated IAM-user and policy. The repository also contain details setup instructions.

It is probably not worth your efforts to use this repository for the backup of a single computer. However, if you need do setup a few - it can be a real time saver.

My original motivation was to properly back my sister's laptop.
Any cloud backup will guard your data against disk/SSD failures, or other things that makes your PC unavailable.
The more challenging scenario is ransom-ware. This is because the ransom-ware will attempt to harm the backups, as well as the original data.
So, I looked for a solution that will address malware. The well known solution is to use "Object locking", which means that the backup software will ask the cloud to disable write or delete of the backup files for a specified amount of months.

The main component of this project is a CDK Python script that deploys the following items:
   - An IAM user that is dedicated to the backup operation. This user have rights only on the S3 bucket used for backup.
   - An S3 bucket that will contain the backup. We will use "S3 Glacier Deep Archive" class, which is the least-expensive AWS option. This bucket supports "Object Lock", which might be used by the backup software, to prevent changes to the backup by a ransom-ware.

## The actual backup software

This repository contains only the cloud-side software. However, here is what I learned, and my choice for the software that runs in the PC-that-will-be-backed-up, in hope it will be useful.

The mission of this software is to copy the data to the cloud.
My criteria are:
  - Free or reasonable one-time fee
  - In case we are backing a Windows machine: support VSS, AKA "Shadow". This allow backup of open-files.
  - Support "Object Locking". Correctly implemented, this is a powerful anti-ransom-ware feature
  - Runs on Windows 
My choice was "arqbackup". Before you choose your backup software, I suggest that you look at-least at the open-source and free restic and Duplicati. 

## Installation

Note: The setup was developed and tested on a Linux machine. Backups can be done from any operating system.

1. This project requires working CDK (the AWS Cloud Developing Kit).

   1.1. Install the AWS CLI, NPM, CDK globally:

   `cd ansible; ./INSTALL`

   Note: you will need to enter your password twice

   1.2. Install the CDK Python dependencies

   ```
   python3 -m venv venv
   . venv/bin/activate
   pip3 install -r requirements.txt 
   ```
   
   1.3. Configure the AWS credentials. 

   You might use a root user or any other user that have rights to create S3 bucket, create an IAM user and create IAM policy.

## Setup the Backup

 1. Deploy at AWS: This will create an IAM user, an S3 bucket and give the user rights on the bucket:
   

   ```
   . venv/bin/activate
   ./create_and_deploy_stack
   ```

  You will need to enter the name of the backup. This might include lower-case letters, digits or dashes ("-").  For example, you might use "george-laptop".

  Note: Running 'create_and_deploy_stack' will print to the screen the details of the created S3 bucket and the aws user. Save this information - you will need it to setup the backup at the client PC.

2. Setup the backup software in the client PC and create a backup plan.

## Useful Links
  -[Duplicati Review](https://www.cloudwards.net/review/duplicati/)
  -[Arq backup Review](https://www.cloudwards.net/review/arq/)
  - [How to setup Immutable Backups with Arq 7](https://www.arqbackup.com/blog/immutable-backups-with-arq-7/)
  - []()
  -[AWS Glacier Pricing Explained](https://www.arqbackup.com/aws-glacier-pricing.html)
  - [CDK cfnBucket usage example](https://github.com/amotz/object-locked-s3-cdk-sample/blob/master/lib/object-locked-s3-cdk-sample-stack.ts)
  - [Another CDK cfnBucket usage example](https://github.com/aws-samples/aws-cdk-examples/blob/9c88ce300037bd0fbc25b900cae8f28a2863046f/typescript/s3-kms-cross-account-replication/stacks/step3-source-account.ts)
  - [S3 policy recomended by Arq Backup](https://www.arqbackup.com/documentation/arq7/English.lproj/createAWSKeyPair.html)
  - [Object-locked s3 CDK sample](https://github.com/amotz/object-locked-s3-cdk-sample/blob/master/lib/object-locked-s3-cdk-sample-stack.ts)
  - [How to define encription for cfnBucket](https://github.com/aws/aws-cdk/issues/4902)

## Author

**Shalom Mitz** - [shalommmitz](https://github.com/shalommmitz)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE ) file for details.

