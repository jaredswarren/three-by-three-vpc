rm setup-firewall-routes.zip
zip -r9 setup-firewall-routes.zip setup_firewall_routes.py
aws s3 cp vpc.yml s3://jarewarr-demo06/
aws s3 cp setup-firewall-routes.zip s3://jarewarr-demo06/
aws cloudformation update-stack --stack-name codecommit-poc --template-body file://code-commit.yml --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM
