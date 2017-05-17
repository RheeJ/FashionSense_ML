#!/bin/bash

echo "Type the name of the classifier followed by [Enter]"
read CLASSIFIER

echo "Type the absolute path of the positive images followed by [Enter]"
read POS_PATH

echo "Type the absolute path of the negative images followed by [Enter]"
read NEG_PATH

docker build -t bccnn_image .
echo "here"
docker run -v $(pwd):/bccnn bccnn_image /bin/bash << EOF
docker exec -i bccnn_image python bcCNN.py -train classifiers $CLASSIFIER $POS_PATH $NEG_PATH
EOF

