# auto-tagging

- 엘라스틱 로드밸런서 Auto Tagging
  - Relation 태그 정보에 표기된 ELB명을 이용하여 EC2, ELB, TARGET_GROUP 탭에서 ELB 연결정보를 파악하기 위함.  
  - Lambda 서비스의 cron 배치서비스를 통해 일 1회 수행하여 정합성 유지.
  - ELB & TARGET GROUP
    - ELB
      - Relation : {LoadBalancerName}
      - Example : WEB-APP
    - TARGET_GROUP
      - Relation : {LoadBalancerName}
      - Example : WEB-APP
    - TARGET_INSTANCE
      - Relation : {LoadBalancerName}
      - Example : WEB-APP