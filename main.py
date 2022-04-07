import boto3

from module.client import *
from module.describe import *
from module.relation import *

from time import time
from pprint import pprint


"""
구현 로직

1.대상 정보 수집
    - ELB 정보 수집 ( describe-load-balancers ) / By *
        - LoadBalancerArn , LoadBalancerName , Type
    - ELB Listener 정보 수집 ( describe-listeners ) / By LoadBalancerArn ( PK : )
        - ListenerArn , LoadBalancerArn , TargetGroupArn , Protocol, Port
    - ELB TargetGroup 정보 수집 ( describe-target-groups ) / By *
        - TargetGroupArn, Protocol, Port , LoadBalancerArns
    - ELB TargetGroup 정보 수집 2 ( describe-target-health ) / By TargetGroupArn
        - Target.Id , Target.Port

2.연결 정보 파악
    - ELB & TargetGroup
        -  TargetGroupArn -> LoadBalancerArn
    - TargetGroup & EC2
        - TargetGroupArn -> Target

3.태깅 대상 선정
    - ELB : LoadBalancerName
    - TargetGroup : LoadBalancerName -  Listener Protocol & port - TargetGroup Protocol & TargetPort
    - EC2 : LoadBalancerName

"""


elb_client = get_client(auth_dict={"profile": "LGES_PRD"}, client_name='elbv2')
begin = time()

load_balancers = all_load_balancers(elb_client=elb_client)
listners = all_listeners(elb_client, load_balancers)
target_groups = all_target_groups(elb_client=elb_client)
targets = all_target_group_health(elb_client, target_groups)

relations = build_relation_list(load_balancers,listners,target_groups,targets)
pprint(relations[2])
# pprint(load_balancers)
# pprint(listners)
# pprint(listners.get("arn:aws:elasticloadbalancing:ap-northeast-2:053520951691:loadbalancer/app/ALB-JENKINS-SERVER/d5a88eb01943b7b7")[0])
# pprint(target_groups)
# pprint(targets)


end = time()

print('(sync) 실행 시간: {0:.3f}초'.format(end-begin))
