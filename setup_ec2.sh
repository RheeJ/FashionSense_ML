#!/bin/bash
# This script will take the an ec2 instance public DNS and set it up for classifier training/hosting

echo "Be sure that the fashion__sense.pem file is in your current working directory"
echo "Type the Public DNS for the EC2 instance followed by [Enter]"

read DNS

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
	
	#mount S3	
	sudo yum -y install automake fuse fuse-devel gcc-c++ git libcurl-devel libxml2-devel make openssl-devel
	cd /home/ec2-user
	git clone https://github.com/s3fs-fuse/s3fs-fuse.git
	mkdir s3_mount
	mkdir s3_mount/image_database
	cd s3fs-fuse
	./autogen.sh
	./configure
	make
	sudo make install
	echo AKIAJW5GZ5OO5JKS64PQ:1rNMaxjPN5U/WKp6TWYYY160iYJQKBniSUefLlG2 > s3_passwd
	chmod 600 s3_image_creds
	
	#change to root to set permissions
	sudo su root 
	echo "user_allow_other" >> /etc/fuse.conf
	echo "addgroup ec2-user fuse" >> /etc/fuse.conf
	/usr/local/bin/s3fs ../s3_mount/imagedataset ../s3_mount -o passwd_file=s3_passwd,allow_other,umask=002
	
	#set up docker
	cd
	sudo yum install -y docker
	sudo service docker start
	sudo usermod -a -G docker ec2-user

	echo "All Done!"
EOF
