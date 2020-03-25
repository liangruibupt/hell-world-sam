# API Gateway HTTP API
Creates an API Gateway HTTP API, which enables you to create RESTful APIs with lower latency and lower costs than REST APIs. 

[API Gateway HTTP API official document](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)

## Manully create HTTP API
[guide document](https://aws.amazon.com/blogs/compute/announcing-http-apis-for-amazon-api-gateway/)
1. create sample lambda function hello-echo which just print hello info and lambda public ip
```python
import json
import requests


def lambda_handler(event, context):
    try:
        ip = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        print(e)
        raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            "location": ip.text.replace("\n", "")
        }),
    }

```
2. Create simple integration on AWS console or use the API Gateway cli
- [console](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop.html#http-api-examples.cli.quick-create)
- aws apigatewayv2 cli
```bash
LAMBDA_ARN=$(aws lambda get-function --function-name  hello-echo \
--query 'Configuration.FunctionArn' --region ${AWS_REGION} --output text)
ApiEndpoint=$(aws apigatewayv2 create-api --name HttpAPIDemo --protocol-type HTTP \
--target ${LAMBDA_ARN} --region ${AWS_REGION} | jq -r '.ApiEndpoint')
statement-id=$(uuidgen)
aws lambda add-permission --statement-id ${statement-id} --action lambda:InvokeFunction \
--function-name ${LAMBDA_ARN} --principal apigateway.amazonaws.com \
--source-arn "arn:aws:execute-api:us-west-1:[your accunt number]:[your gateway id]/" --region ${AWS_REGION}

curl "${ApiEndpoint}/hello-echo"
```
3. 
## Simple Http Api
```bash
sam init -r python3.7 --name http-api-demo
cd http-api-demo
copy sample yaml http-api/simple-httpapi-template.yaml to your http-api-demo location
sam build --template simple-httpapi-template.yaml --region ${AWS_REGION}
cd .aws-sam/build/
sam local invoke --no-event

sam package --template-file simple-httpapi-template.yaml --output-template-file packaged-template.yaml --s3-bucket sam-deployment-ruiliang-zhy --region ${AWS_REGION}

sam deploy --template-file packaged-template.yaml --stack-name http-api-demo --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --region ${AWS_REGION}
```

4. cleanup
```
aws apigatewayv2 create-api delete-api --api-id <api-id>
aws cloudformation delete-stack --stack-name http-api-demo --region ${AWS_REGION}
```