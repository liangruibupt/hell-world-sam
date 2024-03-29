# hell-world-sam

This project to show the demo to build and deploy a serverless application that you can deploy with the SAM CLI.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project demos. You can update the template to add AWS resources through the same deployment process that updates your application code.

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS Toolkit.  

* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

## Getting start Hello World Application
```bash
#Step 1 - Download a sample application
sam init --name hell-world-sam

#Step 2 - Build your application
cd hell-world-sam
sam build --region ${AWS_REGION}

#Step 3 - Deploy your application
sam deploy --guided --region ${AWS_REGION}

#Step 4 - Testing api, replace {HelloWorldApi_URL} with SAM deploy outputs
curl {HelloWorldApi_URL}
#For example: curl https://dm3csbnzsg.execute-api.cn-north-1.amazonaws.com.cn/Prod/hello
sam logs -n HelloWorldFunction --stack-name hell-world-sam --tail --region ${AWS_REGION}

#Step5 - Testing Your Application Locally
## Host Your API Locally 
sam local start-api --port 8080
curl http://127.0.0.1:8080/hello
## Making One-off Invocations 
sam local invoke "HelloWorldFunction" -e events/event.json
sam local generate-event apigateway aws-proxy --body "" --path "hello" --method GET > events/api-event.json
diff events/api-event.json events/event.json
## Unit Test
pip install pytest pytest-mock --user
python -m pytest tests/ -v

##Step6 - clean up
aws cloudformation delete-stack --stack-name hell-world-sam --region ${AWS_REGION}
```
Details of each command can be find in [GettingStart guide](GettingStart.md)

## More example:
- Getting start AWS::Include Transform demo
[AWS::Include Transform demo](SAMIncludeSchema.md)
- Lambda Athourizer for API Gateway demo
[AWS::Serverless Transform demo - Nested Application for Lambda Authorizer](AddLambdaAuthorizer.md)
- Creates an API Gateway HTTP API demo
[Creates an API Gateway HTTP API](HTTPAPIDemo.md)
[Step_Functions_Sample_App for cross region and cross account deployment](Step_Functions_Sample_App.md)

## Resources

[AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
