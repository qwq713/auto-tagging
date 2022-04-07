
def build_relation_list(load_balancers,listeners,target_groups,targets):
    tgg_info = {}
    lb_info = {}
    tg_info = {}
        
    for lb in load_balancers:
        lb_arn = lb.get("LoadBalancerArn")
        lb_name = lb.get("LoadBalancerName")
        
        lb_info[lb_arn] = {}
        lb_info[lb_arn]["LoadBalancerName"] = lb_name
        
        lb_listeners = listeners.get(lb_arn,[])
        for lb_listener in lb_listeners:
            default_action = lb_listener.get("DefaultActions")[0]
            target_group_arn = default_action.get("TargetGroupArn")
            tgg_info[target_group_arn] = {}
            tgg_info[target_group_arn]["LoadBalancerArn"] = lb_arn
            tgg_info[target_group_arn]["LoadBalancerName"] = lb_name
    
    
    for tgg_arn,tg_description in targets.items():
        lb_name = tgg_info.get(tgg_arn,False)

        if not lb_name:
            continue
        
        lb_name = lb_name.get("LoadBalancerName")

        for tg in tg_description:
            tg_id = tg.get("id",False)
            if not tg_id.startswith("i-"):
                continue
            tg_info[tg_id] = lb_name
            
    return {"TargetGroups":tgg_info,
            "LoadBalancers":lb_info,
            "Targets":tg_info}