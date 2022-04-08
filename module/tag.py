
RELATION_TAG_KEY = 'ElbRelation'
RESULT_MESSAGE = "[SUCCESS][{resource}]{arn}={tag_value}"


def tag_load_balancers(elb_client,load_balancers):
    result = []
    
    for lb_arn,lb_info in load_balancers.items():
        lb_name = lb_info.get("LoadBalancerName")    
        elb_client.add_tags(
            ResourceArns=[
                lb_arn
            ],
            Tags=[
                {
                    'Key': RELATION_TAG_KEY,
                    'Value': lb_name
                },
            ]
        )
        result.append(RESULT_MESSAGE.format(resource="ELB",arn=lb_arn,tag_value=lb_name))
    return result


def tag_target_groups(elb_client, target_groups):
    result = []
    
    for tgg_arn,tgg_info in target_groups.items():
        lb_name = tgg_info.get("LoadBalancerName")
        elb_client.add_tags(
            ResourceArns=[
                tgg_arn
            ],
            Tags=[
                {
                    'Key': RELATION_TAG_KEY,
                    'Value': lb_name
                },
            ]
        )
        result.append(RESULT_MESSAGE.format(resource="TGG",arn=tgg_arn,tag_value=lb_name))
    
    return result


def tag_targets(ec2_client, targets):
    result = []
    
    for tg_arn,lb_name in targets.items():
        response = ec2_client.create_tags(
            Resources=[
                tg_arn
            ],
            Tags=[
                {
                    'Key': RELATION_TAG_KEY,
                    'Value': lb_name
                },
            ]
        )
        result.append(RESULT_MESSAGE.format(resource="TG",arn=tg_arn,tag_value=lb_name))
    return result


def tag_resources(elb_client, ec2_client, relations):
    """
    Arguments:
    {"TargetGroups":tgg_info,
    "LoadBalancers":lb_info,
    "Targets":tg_info}
    """

    target_groups = relations.get("TargetGroups", False)
    load_balancers = relations.get("LoadBalancers", False)
    targets = relations.get("Targets", False)
    results = []
    if target_groups:
        ""
        results.extend(tag_target_groups(elb_client, target_groups))

    if load_balancers:
        ""
        results.extend(tag_load_balancers(elb_client, load_balancers))
        

    if targets:
        ""
        results.extend(tag_targets(ec2_client, targets))

    return results