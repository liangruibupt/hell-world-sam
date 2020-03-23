# API Gateway HTTP API
Creates an API Gateway HTTP API, which enables you to create RESTful APIs with lower latency and lower costs than REST APIs. 

[API Gateway HTTP API official document](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)

## Simple Http Api
```bash
sam build --template --region ${AWS_REGION}
cd .aws-sam/build/
sam local invoke --no-event

sam package --template-file template.yaml --output-template-file packaged-template.yaml --s3-bucket sam-deployment-ruiliang-global --region ${AWS_REGION} --profile ${AWS_PROFILE}

sam deploy --template-file packaged-template.yaml --stack-name SimpleAuthExample --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --region ${AWS_REGION} --profile ${AWS_PROFILE}
```