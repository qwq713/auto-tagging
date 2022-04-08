from typing import *

def all_load_balancers(elb_client):
    result = []
    response = elb_client.describe_load_balancers()
    load_balancers = response.get("LoadBalancers", [])
    result.extend(load_balancers)
    next_maker = response.get("NextMarker", False)

    while next_maker:
        response = elb_client.describe_load_balancers(Marker=next_maker)
        load_balancers = response.get("LoadBalancers", [])
        result.extend(load_balancers)
        next_maker = response.get("NextMarker", False)
    return result


def all_listeners(elb_client,all_load_balancers):
    result = {}
    load_balancer_arn_key = "LoadBalancerArn"
    all_load_balancers_arn = [ load_balancer.get(load_balancer_arn_key)  for load_balancer in all_load_balancers if load_balancer.get("LoadBalancerArn",False)]
    
    for arn in all_load_balancers_arn:
        response = elb_client.describe_listeners(LoadBalancerArn=arn)
        listeners = response.get("Listeners",[])
        result[arn] = listeners
    
    return result

def all_target_groups(elb_client):
    result = []
    response = elb_client.describe_target_groups()
    target_groups = response.get("TargetGroups", [])
    result.extend(target_groups)
    next_marker = response.get("NextMarker", False)

    while next_marker:
        response = elb_client.describe_target_groups(Marker=next_marker)
        target_groups = response.get("TargetGroups", [])
        result.extend(target_groups)
        next_marker = response.get("NextMarker", False)
    return result


def all_target_group_health(elb_client, all_target_groups: List[dict]):
    result = {}

    target_group_arn_key = "TargetGroupArn"
    all_target_group_arns = [target_group.get(
        target_group_arn_key) for target_group in all_target_groups]

    for arn in all_target_group_arns:
        response = elb_client.describe_target_health(TargetGroupArn=arn)
        target_health_descriptions = response.get(
            "TargetHealthDescriptions", [])
        targets = [{'id': target_health.get("Target").get("Id"),
                    'port': target_health.get("Target").get("Port")} for target_health in target_health_descriptions if target_health.get("Target")]
        result[arn] = targets

    return result


def all_ec2_instances(ec2_client):
    result = []
    response = ec2_client.describe_instances()
    next_token = response.get("NextToken",False)
    reservations = response.get("Reservations",False)
    if reservations:
        for reserv in reservations:
            instances = reserv.get("Instances",False)
            if instances:
                for instance in instances:
                    if instance.get("State").get("Name") in ["terminated","shutting-down","pending"]:
                        continue
                    result.append(instance)
    
    while next_token:
        response = ec2_client.describe_instances(NextToken=next_token)
        next_token = response.get("NextToken",False)
        reservations = response.get("Reservations",False)
        if reservations:
            for reserv in reservations:
                instances = reserv.get("Instances",False)
                if instances:
                    for instance in instances:
                        if instance.get("State").get("Name") in ["terminated","shutting-down","pending"]:
                            continue
                        result.append(instance)
    return result

def filtered_targets(targets,ec2_instances):
    fileterd_targets = {}
    instances_id_set = { inst.get('InstanceId',False)  for inst in ec2_instances}
    
    for inst_id,lb_name in targets.items():
        if inst_id in instances_id_set:
            fileterd_targets[inst_id] = lb_name    
        
    return fileterd_targets
    
    
    
    