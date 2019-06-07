#!/bin/bash

# CDing to the the directory where vcoclient is. In this case just one directory back.
cd ..

# Storing the Name we should search
NAME=$1 

# Trying to login to current VCO
RET=$(./vcoclient.py --vco=192.168.2.55 login --username=super@velocloud.net --password=vcadm\!n)

if [ $? -eq 1 ]; then
    echo "Login was not successful"
    exit
fi

# Searching for customer name "ACME" and storing the id returned by JSON in a variable in bash
ID=$(./vcoclient.py --vco=192.168.2.55 --output=json customers_get --name=$NAME --filter=id | jq -r ".[].id")

# Check we found customer "ACME" and got an ID from VCO
if [ -z $ID ]; then
    echo "We could not find an id"
    exit
fi

# Executing the edges_get method

RET=$(./vcoclient.py --vco=192.168.2.55 --output=csv edges_get --id=$ID)

# Checking that we do not have an error

if [ $? -eq 1 ]; then
    exit
else
    echo $RET
fi

# Execute the login method 

RET=$(./vcoclient.py --vco=192.168.2.55 logout)

# Checking that we can logout correctly

if [ $? -eq 1 ]; then
    echo $RET
    exit
fi




