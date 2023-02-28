class ECRLoginFailedError(Exception):

    def __init__(self, message="Failed to log into ECR"):
        self.message = message
        super().__init__(self.message)


class DockerPullError(Exception):

    def __init__(self, message="Failed to log into ECR"):
        self.message = message
        super().__init__(self.message)


class DockerTagError(Exception):

    def __init__(self, message="Failed to tag"):
        self.message = message
        super().__init__(self.message)


class DockerPushError(Exception):

    def __init__(self, message="Failed to push"):
        self.message = message
        super().__init__(self.message)


class DockerDeleteImageError(Exception):

    def __init__(self, message="Failed to delete image"):
        self.message = message
        super().__init__(self.message)
