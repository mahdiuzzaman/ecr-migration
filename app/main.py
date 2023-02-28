import re
from helper.logger_initializr import initialize_logger
from awsop.create_repo import CreateRepo
from awsop.list_image_tags import EcrRepoTagList
from helper.compare_list import CompareList
from dockerop.ecr_migration import EcrMigration


from_profile = ''
from_registryId = ''
from_region = ''

to_profile = ''
to_registryId = ''
to_region = ''

from_repositoryName = ''
to_repositoryName = ''

log_file_name = re.sub(r"[^a-zA-z0-9 ]", "_", to_repositoryName)+".log"
logger = initialize_logger(log_file_name)


def main():
    clear_log_file = open(log_file_name, 'w')
    clear_log_file.close()
    CreateRepo(to_registryId, to_repositoryName,
               to_profile, to_region).create_repo()
    from_tag_list = EcrRepoTagList(
        from_registryId, from_repositoryName, from_profile, from_region).get_tag_list()
    to_tag_list = EcrRepoTagList(
        to_registryId, to_repositoryName, to_profile, to_region).get_tag_list()
    final_tag_list = CompareList(
        from_tag_list, to_tag_list).compare_and_remove_commons()
    if final_tag_list != None:
        logger.info(
            f"Length of from_tag_list = {len(from_tag_list)}  Length of to_tag_list = {len(to_tag_list)}  Length of final_tag_list = {len(final_tag_list)}")
        migration = EcrMigration(
            final_list=final_tag_list,
            from_registryId=from_registryId,
            from_repositoryName=from_repositoryName,
            from_profile_name=from_profile,
            from_region_name=from_region,
            to_registryId=to_registryId,
            to_repositoryName=to_repositoryName,
            to_profile_name=to_profile,
            to_region_name=to_region)
        migration.copy_images()
    else:
        logger.info("All images from old repo already exist in new repo")


if __name__ == '__main__':
    main()
