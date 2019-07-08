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

# Trying to get all customers for MSP from VCO
RET=$(vcoclient.py --output=json msp_customers_get | jq '.[].id' )
if [ $? -eq 1 ]; then
    echo $RET
    exit 1
fi

# Executing the edges_get method 

SEARCH=$1
for ID in  $RET; do
    RET=$(vcoclient.py --output=csv edges_get --search=$SEARCH --id=$ID)
    if [ ${#RET} -ge 3 ]; then
        echo "'$ID' found '$SEARCH':"
        echo $RET
    fi
done
# Execute the logout method 
RET=$(vcoclient.py logout)

# Checking that we can logout correctly

if [ $? -eq 1 ]; then
    echo $RET
    exit 1
fi

