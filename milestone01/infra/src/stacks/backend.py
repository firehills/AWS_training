import os
from pathlib import Path
from constructs import Construct
from aws_cdk import Stack, CfnOutput
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_iam as iam
from aws_cdk import aws_apprunner as apprunner
from aws_cdk import RemovalPolicy, Aws
from aws_cdk import aws_ecr_assets as ecr_assets
import cdk_ecr_deployment as ecr_deploy

# Note - Repository name must start with a letter and can only contain lowercase letters, numbers, hyphens, underscores, periods and forward slashes
_APP_NAME="appname_milestone01"

# this will be different for everyone so
# make sure to change it
_SECRET_ID_SUFFIX = "okkwPR"

class BackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        path_to_docker_dir = Path(os.getcwd()).parent.joinpath("backend/python")
        print("Path =" + str(path_to_docker_dir))


        # Step 1:
        print("Step 1 - ECR Repo")
        # We need a ECR Repo
        backend_repo = self._create_ecr_repo()

        # Step 2
        print("Step 2 - Building Docker")
        # Build the docker image
        image = self._create_docker_image()
        target_docker_image = (
            f"{Aws.ACCOUNT_ID}.dkr.ecr.{Aws.REGION}.amazonaws.com/{_APP_NAME}:latest"
        )

        # Step 3:
        print("Step 3 - Pushing to ECR")
        # Push the docker image to ECR
        _ = ecr_deploy.ECRDeployment(
            self,
            "deploy-docker-image",
            src=ecr_deploy.DockerImageName(image.image_uri),
            dest=ecr_deploy.DockerImageName(target_docker_image),
        )


        # Step 4:
        print("Step 4 - Create Roles")
        # Create a role that can access ECR
        app_runner_access_role = self._create_apprunner_access_role()
        app_runner_instance_role = self._create_apprunner_instance_role()

        # Step 5:
        print("Step 5 - Create Roles")
        app_runner = self._create_app_runner(
            app_runner_access_role,
            app_runner_instance_role,
            target_docker_image,
            )


        CfnOutput(self, 
                  "backend-url", 
                  value=f"https://{app_runner.attr_service_url}",
                  description="Milestone01BackendURL")
        
        CfnOutput(self, 
                  "backend-image", 
                  value=image.image_uri,
                  description="Milestone01 backend registry url"
                  )

    def _create_ecr_repo(self):
       
        repository = ecr.Repository(
            self,
            "backend-repo",
            repository_name=_APP_NAME,
            image_scan_on_push=True,
            removal_policy=RemovalPolicy.DESTROY,
            empty_on_delete=True,
        )

        return repository
    
    def _create_docker_image(self) -> ecr_assets.DockerImageAsset:

        # path to Dockerfile
        path_to_docker_dir = Path(os.getcwd()).parent.joinpath("backend/python")
        asset = ecr_assets.DockerImageAsset(
            self,
            "backend-app-image",
            directory=str(path_to_docker_dir),
            file="Dockerfile",
            asset_name="backend-app-image",
            platform=ecr_assets.Platform.LINUX_AMD64,
            cache_disabled=True,
        )
        return asset
    
    def _create_ecr_repo(self):
      
        repository = ecr.Repository(
            self,
            "backend-repo",
            repository_name=_APP_NAME,
            image_scan_on_push=True,
            removal_policy=RemovalPolicy.DESTROY,
            empty_on_delete=True,
        )

        return repository
    

    def _create_apprunner_access_role(self) -> iam.Role:
        role = iam.Role(
            self,
            "access-role",
            assumed_by=iam.ServicePrincipal("build.apprunner.amazonaws.com"),
            description="Milestone01 ApprunnerAccessrole",
            inline_policies={
                "access-policy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "ecr:GetAuthorizationToken",
                            ],
                            resources=["*"],
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "ecr:BatchCheckLayerAvailability",
                                "ecr:GetDownloadUrlForLayer",
                                "ecr:GetRepositoryPolicy",
                                "ecr:DescribeRepositories",
                                "ecr:ListImages",
                                "ecr:DescribeImages",
                                "ecr:BatchGetImage",
                                "ecr:GetLifecyclePolicy",
                                "ecr:GetLifecyclePolicyPreview",
                                "ecr:ListTagsForResource",
                                "ecr:DescribeImageScanFindings",
                            ],
                            resources=[
                                f"arn:aws:ecr:{Aws.REGION}:{Aws.ACCOUNT_ID}:repository/{_APP_NAME}"
                            ],
                        ),
                    ]
                )
            },
        )

        return role

    def _create_apprunner_instance_role(self) -> iam.Role:
        role = iam.Role(
            self,
            "instance-role",
            description="Milestone01 ApprunnerinstanceRole",
            assumed_by=iam.ServicePrincipal("tasks.apprunner.amazonaws.com"),
            inline_policies={
                "instance-policy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "secretsmanager:GetResourcePolicy",
                                "secretsmanager:GetSecretValue",
                                "secretsmanager:DescribeSecret",
                                "secretsmanager:ListSecretVersionIds",
                            ],
                            resources=[
                                f"arn:aws:secretsmanager:{Aws.REGION}:{Aws.ACCOUNT_ID}:secret:*"
                            ],
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "secretsmanager:ListSecrets",
                            ],
                            resources=["*"],
                        ),
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=["ssm:GetParameters"],
                            resources=[
                                f"arn:aws:ssm:{Aws.REGION}:{Aws.ACCOUNT_ID}:parameter/*"
                            ],
                        ),
                    ]
                )
            },
        )

        return role
    

    def _create_app_runner(
        self,
        app_runner_access_role: iam.Role,
        app_runner_instance_role: iam.Role,
        target_docker_image: str,
    ):
        service = apprunner.CfnService(
            self,
            "backend-service",
            service_name="ai-cop-aws-backend",
            instance_configuration=apprunner.CfnService.InstanceConfigurationProperty(
                instance_role_arn=app_runner_instance_role.role_arn,
            ),
            source_configuration=apprunner.CfnService.SourceConfigurationProperty(
                authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                    access_role_arn=app_runner_access_role.role_arn,
                ),
                image_repository=apprunner.CfnService.ImageRepositoryProperty(
                    image_identifier=target_docker_image,
                    image_repository_type="ECR",
                    image_configuration=apprunner.CfnService.ImageConfigurationProperty(
                        port="8000",
                        runtime_environment_secrets=[
                            apprunner.CfnService.KeyValuePairProperty(
                                name="A_CONFIG",
                                value=f"arn:aws:ssm:{Aws.REGION}:{Aws.ACCOUNT_ID}:parameter/ai-cop-backend-config",
                            ),
                            apprunner.CfnService.KeyValuePairProperty(
                                name="SECRET_MESSAGE",
                                value=f"arn:aws:secretsmanager:{Aws.REGION}:{Aws.ACCOUNT_ID}:secret:/ai-cop/the-secret-{_SECRET_ID_SUFFIX}",
                            ),
                        ],
                    ),
                ),
                auto_deployments_enabled=True,
            ),
            health_check_configuration=apprunner.CfnService.HealthCheckConfigurationProperty(
                path="/health",
                protocol="HTTP",
            ),
        )

        return service