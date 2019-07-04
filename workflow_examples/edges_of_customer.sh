#!/bin/bash

# Uncomment this line to export right VCO_HOST, VCO_USER and VCO_PASS
#export VCO_HOST=""
#export VCO_USER=""
#export VCO_PASS=""

# Trying to login to current VCO
RET=$(vcoclient.py login --no-operator)

if [ $? -eq 1 ]; then
    echo $RET
    exit 1
fi

# Trying to get any random customer for MSP from VCO
ID=$(vcoclient.py --output=json msp_customers_get | jq '.[].id' | shuf | head -n 1 )
if [ $? -eq 1 ] && [ ${#ID} > 0 ]; then
    echo $ID
    exit 1
fi

# Executing the edges_get method 

RET=$(vcoclient.py --output=csv edges_get --search=* --filters=interface --id=$ID)

# Checking that we do not have an error
echo $RET
if [ $? -eq 1 ]; then
    exit 1
fi

# Execute the logout method 
RET=$(vcoclient.py logout)

# Checking that we can logout correctly

if [ $? -eq 1 ]; then
    echo $RET
    exit 1
fi




