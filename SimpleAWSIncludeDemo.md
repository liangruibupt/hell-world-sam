# Simple AWS::Include demo
## Step 1 - Create a sample application
```bash
mkdir -p sam-include-demo
mkdir -p sam-include-demo/child
mkdir -p sam-include-demo/child/lambda
```

## Step 2 - Prepare tempalte
1. sam-include-demo/root_template.yaml
```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31

Resources:
  Child:
    Type: AWS::Serverless::Application
    Properties:
      Location: child/child_template.yaml
```

2. sam-include-demo/child/child_template.yaml
```yaml
AWSTemplateFormatVersion: 2010-09-09
Transform: AWS::Serverless-2016-10-31

Resources:
  SampleFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: lambda/
      Handler: app.lambda_handler
      Runtime: python3.7

  SampleAPI:
    Type: AWS::Serverless::Api
    Properties:
      Name: Sample
      StageName: dev
      DefinitionBody:
        Fn::Transform:
          Name: AWS::Include
          Parameters:
            Location: openapi.yaml

  SampleFunctionPermission:
    Type: AWS::Lambda::Permission
    Properties:
      Action: lambda:InvokeFunction
      FunctionName: !Ref SampleFunction
      Principal: apigateway.amazonaws.com
```

3. sam-include-demo/child/openapi.yaml
```yaml
openapi: 3.0.1

info:
  title: Sample API
  version: '2019-03-22'

paths:
  /sample:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object

      x-amazon-apigateway-integration:
        uri:
          Fn::Sub: arn:${AWS::Partition}:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${SampleFunction.Arn}/invocations
        responses:
          default:
            statusCode: '200'
        passthroughBehavior: when_no_match
        httpMethod: POST
        contentHandling: CONVERT_TO_TEXT
        type: aws_proxy
```

4. sam-include-demo/child/lambda/app.py
```python
import json

# import requests


def lambda_handler(event, context):
    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
```

## Step 3 - Package and deploy template
```bash
# SAM package
cd sam-include-demo
sam build --template root_template.yaml --region ${AWS_REGION}
sam package --template-file root_template.yaml --output-template-file packaged.yaml --s3-bucket sam-deployment-ruiliang-zhy --region ${AWS_REGION}

# SAM validate
sam validate --template packaged.yaml --region ${AWS_REGION}
sam validate --template child/child_template.yaml --region ${AWS_REGION}

# SAM deploy
sam deploy --template-file packaged.yaml --stack-name sam-include-demo --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --region ${AWS_REGION}

```

## China region failed:
```bash
CloudFormation events from changeset
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ResourceStatus                              ResourceType                                LogicalResourceId                           ResourceStatusReason
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE_IN_PROGRESS                          AWS::CloudFormation::Stack                  Child                                       -
CREATE_IN_PROGRESS                          AWS::CloudFormation::Stack                  Child                                       Resource creation Initiated
CREATE_FAILED                               AWS::CloudFormation::Stack                  Child                                       Embedded stack arn:aws-
                                                                                                                                    cn:cloudformation:cn-
                                                                                                                                    northwest-1:876820548815:stack/sam-
                                                                                                                                    include-demo-Child-HZD46SHY3KMY/b7047060-
                                                                                                                                    6cc5-11ea-b159-067d8bb6a36e was not
                                                                                                                                    successfully created: No transform named
                                                                                                                                    AWS::Include found.
ROLLBACK_IN_PROGRESS                        AWS::CloudFormation::Stack                  sam-include-demo                            The following resource(s) failed to
                                                                                                                                    create: [Child]. . Rollback requested by
                                                                                                                                    user.
DELETE_IN_PROGRESS                          AWS::CloudFormation::Stack                  Child                                       -
DELETE_COMPLETE                             AWS::CloudFormation::Stack                  Child                                       -
ROLLBACK_COMPLETE                           AWS::CloudFormation::Stack                  sam-include-demo                            -
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

## Step 4 - Testing
```bash
Testing api, replace {Api_URL} with SAM deploy outputs
curl {Api_URL}
#For example: curl https://dm3csbnzsg.execute-api.cn-north-1.amazonaws.com.cn/Prod/hello
```

## Step 5 - clean up
aws cloudformation delete-stack --stack-name sam-include-demo --region ${AWS_REGION}