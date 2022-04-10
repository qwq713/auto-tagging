#!/bin/bash

SUCCESS=0
FAIL=1

zipfile="lambda.zip"
zip -r $zipfile ./module ./main.py ./lambda_function.py

if [ -f "$zipFile" ]; then  
    exit $SUCCESS
else
    exit $FAIL
fi

# aws lambda update-function-code --function-name auto-tagging --zip-file fileb://$zipfile --profile TEST