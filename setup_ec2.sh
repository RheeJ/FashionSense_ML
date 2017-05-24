#!/bin/bash
# This script will take the an ec2 instance public DNS and set it up for classifier training/hosting

echo "Be sure that aws cli is configured"

#DNS=$(aws ec2 describe-instances --filter "Name=instance-state-name,Values=running" --output text --query 'Reservations[*].Instances[*].PublicDnsName')
echo "Enter Public DNS of the instance"
read DNS

AZ=$(aws ec2 describe-instances --filter "Name=dns-name,Values=$DNS" --output text --query 'Reservations[*].Instances[*].Placement.AvailabilityZone')
#echo "Enter Availability Zone"
#read AZ

ID=$(aws ec2 describe-instances --filter "Name=dns-name,Values=$DNS" --output text --query 'Reservations[*].Instances[*].InstanceId')
#echo "Enter instance ID"
#read ID

#S_ID=$(aws ec2 describe-snapshots --filter "Name=tag-key,Values=db" --output text --query 'Snapshots[*].SnapshotId')
echo "Enter the Snapshot ID"
read S_ID
echo $AZ
echo $S_ID
aws ec2 create-volume --snapshot-id $S_ID --availability-zone $AZ
sleep 5

V_ID=$(aws ec2 describe-volumes --filter "Name=snapshot-id,Values=$S_ID" --output text --query 'Volumes[*].VolumeId')
#echo "Enter Volume ID"
#read V_ID

aws ec2 attach-volume --volume-id $V_ID --instance-id $ID --device /dev/sdf

AKEY=AKIAILT4ZF45C6IYWSMQ
SKEY=DC9tD+MRSiY9M+yKQgefjDjJaUp67l9FOl6IxZOO

#scp this file ssh into the instance
ssh -i fashion__sense.pem ec2-user@$DNS << EOF
	
	#install updates
	sudo yum -y update
	

	#install git
	sudo yum -y install git-all
	

	#set up the ML repo
	git clone https://github.com/RheeJ/FashionSense_ML.git
	cd FashionSense_ML
	rm -r binary_classifier_CNN
	git clone https://github.com/sgp715/binary_classifier_CNN.git

	#set up virtual environment
	virtualenv training_env
	source training_env/bin/activate
	pip install --upgrade pip
	sudo yum -y install gcc
	
	pip install -r requirements.txt
	if [ "$S_ID" != "0" ]	
	then
		aws configure set aws_access_key_id $AKEY
		aws configure set aws_secret_access_key $SKEY
		aws configure set region $AZ
		sudo mkdir /data
		sudo mount /dev/xvdf /data
	else
		#mount S3	
		sudo yum -y install automake fuse fuse-devel gcc-c++ git libcurl-devel libxml2-devel make openssl-devel
		cd /home/ec2-user
		git clone https://github.com/s3fs-fuse/s3fs-fuse.git
		mkdir s3_mount
		cd s3fs-fuse
		./autogen.sh
		./configure
		make
		sudo make install
		echo AKIAJW5GZ5OO5JKS64PQ:1rNMaxjPN5U/WKp6TWYYY160iYJQKBniSUefLlG2 > s3_passwd
		chmod 600 s3_passwd
	
		#change to root to set permissions
		sudo su root 
		echo "user_allow_other" >> /etc/fuse.conf
		echo "addgroup ec2-user fuse" >> /etc/fuse.conf
		/usr/local/bin/s3fs imagedataset ../s3_mount -o passwd_file=s3_passwd,allow_other,umask=002
	fi

	#set up docker
	cd
	sudo yum install -y docker
	sudo service docker start
	sudo usermod -a -G docker ec2-user
	echo "All Done!"
EOF

ssh -i fashion__sense.pem ec2-user@$DNS
