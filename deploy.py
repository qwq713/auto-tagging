from pprint import pprint
import shutil
import zipfile
from datetime import datetime
from module import client

zip_fname="lambda.zip"
now_datetime = datetime.strftime(datetime.now(),"%Y-%m-%d-%H-%M-%S")
function_name = "auto-tagging"

print(f"move lambda.zip to lambda.zip.{now_datetime}")
try:
    shutil.move(zip_fname,f"{zip_fname}.{now_datetime}")
except:
    print(f"don't exist {zip_fname} file.")

print("build lambda.zip...")

lambda_zip = zipfile.ZipFile(zip_fname,"w")
lambda_zip.write(f"./module")
lambda_zip.write(f"./module/__init__.py")
lambda_zip.write(f"./module/client.py")
lambda_zip.write(f"./module/describe.py")
lambda_zip.write(f"./module/relation.py")
lambda_zip.write(f"./module/tag.py")
lambda_zip.write(f"./main.py")
lambda_zip.write(f"./lambda_function.py")
lambda_zip.close()

with open(f'{zip_fname}', 'rb') as f:
    zipped_code = f.read()


lambda_client = client.get_client(auth_dict={}, client_name='lambda')

response = lambda_client.update_function_code(
    FunctionName=function_name,
    ZipFile=zipped_code)

pprint(response)