# Invoking AWS Lambda by API Gateway Endpoint using IaC code in Pulumi

This project demonstrates how to create an AWS Lambda function and an Amazon API Gateway to invoke the Lambda function using Pulumi.

## Table of Contents
1. [Prerequisites](#Prerequisites)
2. [Getting Started](#GettingStarted)
3. [Deploying](#Deploying)
4. [Accessing](#Accessing)
5. [Security](#Security)
6. [License](#License)

## Prerequisites <a name="Prerequisites"></a>

[Pulumi](https://www.pulumi.com/docs/iac/get-started/aws/) installed and configured on your machine

[AWSCredentials] (https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-configure.html) configured on your machine

## Getting Started <a name="GettingStarted"></a>

1. Clone the repository: 

```bash
 git clone git@github.com:aws-samples/invoke-lambda-from-apigw-pulumi.git    
```

2. Navigate to the project directory:

```bash
 cd invoke-lambda-from-apigw-pulumi
```

3. Goto __main__.py line 48 and pdate the source_arn parameter in the lambda_permission resource to use your own AWS account ID and region

```bash
 source_arn=f"arn:aws:execute-api:us-east-1:111122223333:*/*/GET/*"  
```
4. Create a new Pulumi stack:

```bash
 pulumi stack init dev-stack
```

5. Deploy the Infrastructure

```bash
 pulumi up 
```

## Accessing <a name="Accessing"></a>

1. Goto created APi GW in AWS console and select Stages-->dev-->myresource-->GET and fetch the Invoke URL to open in a browser

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.