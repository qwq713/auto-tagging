from typing import *
import asyncio
import functools


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
