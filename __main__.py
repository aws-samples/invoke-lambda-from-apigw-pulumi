import json
import pulumi
import pulumi_aws as aws

# Create an IAM role for the Lambda function
lambda_role = aws.iam.Role("lambdaRole",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com",
            },
            "Effect": "Allow",
        }],
    })
)

# Attach the AWSLambdaBasicExecutionRole policy to the Lambda role
lambda_role_policy_attachment = aws.iam.RolePolicyAttachment("lambdaRolePolicy",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)


# Create the Lambda function
lambda_function = aws.lambda_.Function("helloWorldLambda",
    role=lambda_role.arn,
    runtime="python3.8",
    handler="index.lambda_handler",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda")
    })
)



# Create an API Gateway REST API
api = aws.apigateway.RestApi("myApi",
    description="API Gateway for invoking Lambda"
)

# Grant API Gateway permission to invoke the Lambda function
lambda_permission = aws.lambda_.Permission("apiGatewayInvoke",
    action="lambda:InvokeFunction",
    function=lambda_function.name,
    principal="apigateway.amazonaws.com",
    source_arn=f"arn:aws:execute-api:us-east-1:111122223333:*/*/GET/*"
)

# Create a resource under the API
resource = aws.apigateway.Resource("myResource",
    rest_api=api.id,
    parent_id=api.root_resource_id,
    path_part="myresource"
)

# Create a method for the resource
method = aws.apigateway.Method("myMethod",
    rest_api=api.id,
    resource_id=resource.id,
    http_method="GET",
    authorization="NONE"
)

# Integrate the method with the Lambda function
integration = aws.apigateway.Integration("lambdaIntegration",
    rest_api=api.id,
    resource_id=resource.id,
    http_method=method.http_method,
    integration_http_method="POST",
    type="AWS_PROXY",
    uri=lambda_function.invoke_arn
)

# Deploy the API
deployment = aws.apigateway.Deployment("myDeployment",
    rest_api=api.id,
    stage_name="dev",
    opts=pulumi.ResourceOptions(depends_on=[integration])
)

pulumi.export("url", deployment.invoke_url)
