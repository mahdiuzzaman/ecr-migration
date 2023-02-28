import boto3 as b3


class EcrRepoTagList:
    def __init__(self, registryId, repositoryName, profile_name, region_name) -> None:
        self.registryId = registryId
        self.repositoryName = repositoryName
        self.session = b3.Session(
            profile_name=profile_name, region_name=region_name)
        self.client = self.session.client('ecr')
        self.tag_list = []

    def get_tag_list(self, token=None):
        image_list = None
        if token is None:
            image_list = self.client.list_images(
                registryId=self.registryId,
                repositoryName=self.repositoryName,
                maxResults=100
            )
        else:
            image_list = self.client.list_images(
                registryId=self.registryId,
                repositoryName=self.repositoryName,
                maxResults=100,
                nextToken=token
            )
        for i in image_list['imageIds']:
            if 'imageTag' in i:
                self.tag_list.append(i.get('imageTag'))
        if 'nextToken' in image_list:
            self.get_tag_list(token=image_list['nextToken'])
            return self.tag_list
        else:
            return self.tag_list
