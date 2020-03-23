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
