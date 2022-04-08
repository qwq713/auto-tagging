from module.client import *
from module.describe import *
from module.relation import *
from module.tag import *
from time import time

from pprint import pprint

begin = time()

elb_client = get_client(auth_dict={"profile": "TEST"}, client_name='elbv2')
ec2_client = get_client(auth_dict={"profile": "TEST"}, client_name='ec2')

load_balancers = all_load_balancers(elb_client)
listners = all_listeners(elb_client, load_balancers)
target_groups = all_target_groups(elb_client=elb_client)
ec2_instances = all_ec2_instances(ec2_client)
targets = all_target_group_health(elb_client, target_groups)

relations = build_relation_list(load_balancers,listners,target_groups,targets)
relations["Targets"] = filtered_targets(relations.get("Targets"),ec2_instances)

tagged_list = tag_resources(elb_client, ec2_client, relations)

pprint(tagged_list)

end = time()
print('(sync) 실행 시간: {0:.3f}초'.format(end-begin))
