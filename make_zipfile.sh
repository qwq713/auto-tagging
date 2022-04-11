#!/bin/bash

zipfile="lambda.zip"
zip -r $zipfile ./module ./main.py ./lambda_function.py