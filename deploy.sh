#!/bin/bash

zipfile="lambda.zip"
rm $zipfile
zip -r $zipfile ./module ./main.py ./lambda_function.py

echo "wait until make $zipfile"

sleep 1

aws lambda update-function-code --function-name auto-tagging --zip-file fileb://$zipfile --profile TEST