import subprocess
import logging
from helper.custom_exception import *

logger = logging.getLogger()


class EcrMigration:
    def __init__(self, from_registryId, from_repositoryName, from_profile_name, from_region_name, to_registryId, to_repositoryName, to_profile_name, to_region_name, final_list) -> None:
        self.from_registryId = from_registryId
        self.from_repositoryName = from_repositoryName
        self.from_profile_name = from_profile_name
        self.from_region_name = from_region_name
        self.to_registryId = to_registryId
        self.to_repositoryName = to_repositoryName
        self.to_profile_name = to_profile_name
        self.to_region_name = to_region_name
        self.from_base = f'{from_registryId}.dkr.ecr.{from_region_name}.amazonaws.com/{from_repositoryName}'
        self.to_base = f'{to_registryId}.dkr.ecr.{to_region_name}.amazonaws.com/{to_repositoryName}'
        self.final_list = final_list

    def _docker_login(self):
        from_login = subprocess.run(
            ["sh", "-c", f"aws ecr get-login-password --region {self.from_region_name} --profile {self.from_profile_name} | docker login --username AWS --password-stdin {self.from_registryId}.dkr.ecr.{self.from_region_name}.amazonaws.com"],  capture_output=True, encoding='utf-8')

        if (from_login.returncode == 0):
            logger.info(
                f"Log in to Old ECR for account {self.from_registryId}, Region {self.from_region_name}")
        else:
            raise ECRLoginFailedError(
                f"Failed to log in into ECR for account {self.from_registryId}, Region {self.from_region_name}, {from_login.stderr}")

        to_login = subprocess.run(
            ["sh", "-c", f"aws ecr get-login-password --region {self.to_region_name} --profile {self.to_profile_name} | docker login --username AWS --password-stdin {self.to_registryId}.dkr.ecr.{self.to_region_name}.amazonaws.com"], capture_output=True, encoding='utf-8')
        if (to_login.returncode == 0):
            logger.info(
                f"Log in to New ECR account {self.to_registryId}, Region {self.to_region_name}")
        else:
            raise ECRLoginFailedError(
                f"Failed to log in into ECR for account {self.to_registryId}, Region {self.to_region_name}")

    def _docker_pull(self, tag):
        pull = subprocess.run(["sh", "-c", f"docker pull {self.from_base}:{tag}"],
                              capture_output=True, encoding='utf-8')
        if (pull.returncode == 0):
            logger.info(f"Pulled {self.from_base}:{tag}")
        else:
            raise DockerPullError(f"Failed to pull {self.from_base}:{tag}")

    def _docker_tag(self, tag):
        tagging = subprocess.run(
            ["sh", "-c", f"docker tag {self.from_base}:{tag} {self.to_base}:{tag}"], capture_output=True, encoding='utf-8')
        if tagging.returncode == 0:
            logger.info(
                f"Retagging {self.from_base}:{tag} to {self.to_base}:{tag}")
        else:
            raise DockerTagError(
                f"Failed to tag {self.from_base}:{tag} to {self.to_base}:{tag}")

    def _docer_push(self, tag):
        push = subprocess.run(["sh", "-c", f"docker push {self.to_base}:{tag}"],
                              capture_output=True, encoding='utf-8')
        if push.returncode == 0:
            logger.info(f"Pushed {self.to_base}:{tag}")
        else:
            raise DockerPushError(f"Failed to push {self.to_base}:{tag}")

    def _docker_delete_image(self, tag):
        delete1 = subprocess.run(
            ["sh", "-c", f"docker rmi -f {self.from_base}:{tag}"], capture_output=True, encoding='utf-8')
        if delete1.returncode == 0:
            logger.info(f"Deleted {self.from_base}:{tag}")
        else:
            raise DockerDeleteImageError(
                f"Failed to delte {self.from_base}:{tag}")
        delete2 = subprocess.run(
            ["sh", "-c", f"docker rmi -f {self.to_base}:{tag}"], capture_output=True, encoding='utf-8')
        if delete2.returncode == 0:
            logger.info(f"Deleted {self.to_base}:{tag}")
        else:
            raise DockerDeleteImageError(
                f"Failed to delte {self.to_base}:{tag}")

    def copy_images(self):
        try:
            temp_list = []
            count_image = 1
            self._docker_login()
            for tag in self.final_list:
                self._docker_pull(tag)
                self._docker_tag(tag)
                self._docer_push(tag)
                logger.info(
                    f"###########    Finished pusing image no {count_image} with tag: {tag}   ###################")
                temp_list.append(tag)
                if len(temp_list) == 50:
                    for tag in temp_list:
                        self._docker_delete_image(tag)
                    temp_list = []
                count_image = count_image+1
        except ECRLoginFailedError as e:
            logger.info(e)
        except DockerPullError as e:
            logger.info(e)
        except DockerTagError as e:
            logger.info(e)
        except DockerPushError as e:
            logger(e)
        except DockerDeleteImageError as e:
            logger(e)
