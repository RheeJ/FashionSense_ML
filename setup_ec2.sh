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

	echo "All Done!"
EOF
