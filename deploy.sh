#!/bin/bash
zipfile="lambda.zip"
now_datetime=`+%Y-%m-%d-%H-%M-%S`
function_name="auto-tagging"


mv $zipfile "$zipfile.$now_datetime"

zip -r $zipfile ./module ./main.py ./lambda_function.py

output=`aws lambda update-function-code \
--function-name $function_name \
--zip-file fileb://$zipfile`

echo $output