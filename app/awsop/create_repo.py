import boto3 as b3
import logging
import time

logger = logging.getLogger()


class CreateRepo:
    def __init__(self, registryId, repositoryName, profile_name, region_name) -> None:
        self.registryId = registryId
        self.repositoryName = repositoryName
        self.session = b3.Session(
            profile_name=profile_name, region_name=region_name)
        self.client = self.session.client('ecr')

    def create_repo(self):
        try:
            response = self.client.create_repository(
                registryId=self.registryId,
                repositoryName=self.repositoryName,
                imageScanningConfiguration={
                    'scanOnPush': True
                }
            )
        except Exception as e:
            logger.info(
                f"{self.repositoryName} already exist, skipping repo creation")
