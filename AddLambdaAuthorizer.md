# AWS::Serverless Transform demo - Lambda Athourizer for API Gateway

[Official AWS::Serverless Transform docuemnt](https://docs.amazonaws.cn/en_us/AWSCloudFormation/latest/UserGuide/transform-aws-serverless.html)

In this section, I want to extend the sample API created in [GettingStart](GettingStart.md) by adding an authorization mechanism to add some security.
API Gateway supports several methods for doing this:
- IAM Permissions
- Lambda Authorizers
- Cognito User Pools
- API Keys
In this case, I want to leverage Lambda Authorizers to provide a basic form of HTTP Basic Auth. 

## Building a sample application
```bash
sam init -r python3.7 --name lambda-athourizer-sam
cd lambda-athourizer-sam
sam build --region ${AWS_REGION}
cd .aws-sam/build/
sam local invoke --no-event
```

## Include nested application
You can search an existing serverless application that provide 'HTTP Basic Auth' from AWS Serverless Application Repository or AWS Lambda console. Type the "http basic auth", you can find the 'lambda-authorizer-basic-auth'. 

The source code in https://github.com/dougalb/lambda-authorizer-basic-auth

1. Include The SAM Resource

    Add the lambdaauthorizerbasicauth to template as new Resources
```yaml
  lambdaauthorizerbasicauth:
    Type: AWS::Serverless::Application
    Properties:
      Location:
        ApplicationId: arn:aws:serverlessrepo:us-east-1:560348900601:applications/lambda-authorizer-basic-auth
        SemanticVersion: 0.2.0
```        

2. Create an AWS::Serverless::Api resource

    Create an AWS::Serverless::Api resource and then configure the authorizer with the FunctionArn attribute set to '!GetAtt lambdaauthorizerbasicauth.Outputs.LambdaAuthorizerBasicAuthFunction'.

```yaml
MyApi:
  Type: AWS::Serverless::Api
  Properties:
    StageName: Prod      
    Auth:
      DefaultAuthorizer: MyLambdaRequestAuthorizer
      Authorizers:
        MyLambdaRequestAuthorizer:
          FunctionPayloadType: REQUEST
          FunctionArn: !GetAtt lambdaauthorizerbasicauth.Outputs.LambdaAuthorizerBasicAuthFunction
          Identity:
            Headers:
              - Authorization
```

3. Add the event to existed hello-world API

    Notice the last 3 lines to add LambdaRequestAuthorizer to hello-world API
```yaml
  HelloWorldFunction:
    Type: AWS::Serverless::Function 
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.7
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
            RestApiId: !Ref MyApi
            Auth:
              Authorizers: MyLambdaRequestAuthorizer
```

4. Create the new outputs
```yaml
Outputs:
  HelloWorldApi:
    Description: "API Gateway endpoint URL for Prod stage for Hello World function"
    Value: !Sub "https://${MyApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/hello/"
```

## Build and deploy the API
```bash
sam package --template-file template.yaml --output-template-file packaged-template.yaml --s3-bucket sam-deployment-ruiliang-global --region ${AWS_REGION} --profile ${AWS_PROFILE}

sam deploy --template-file packaged-template.yaml --stack-name SimpleAuthExample --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --region ${AWS_REGION} --profile ${AWS_PROFILE}
```

## Testing the authorizer
1. Create a user and its password in DynamoDB table 'lambda-authorizer-basic-auth-users' created by Lambda Authorizer
```json
{
  "username": "foo",
  "password": "passw0rd"
}
```
2. Testing. Set the {API_URL} by SAM output
```bash
curl -u foo:passw0rd ${API_URL}
{"message": "hello world"}

curl -u foo:bar ${API_URL}
{"Message":"User is not authorized to access this resource with an explicit deny"}
```

## Clean up
```bash
aws cloudformation delete-stack --stack-name SimpleAuthExample --region ${AWS_REGION} --profile ${AWS_PROFILE}
```