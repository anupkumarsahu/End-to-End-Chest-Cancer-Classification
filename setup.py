from setuptools import find_packages, setup

REQUIREMENT_FILE_NAME = "requirements.txt"
REMOVE_PACKAGE = "-e ."

__version__ = "0.0.0"
__license__ = "MIT"

REPO_NAME = "End-to-End-Chest-Cancer-Classification"
AUTHOR_USER_NAME = "anupkumarsahu"
SRC_REPO = "cnnClassifier"
AUTHOR_EMAIL = "anup.sahu@gmail.com"


def get_requirement_list(requirement_filename=REQUIREMENT_FILE_NAME) -> list:
    try:
        requirement_list = None
        with open(requirement_filename) as requirement_file:
            requirement_list = [
                requirement.replace("\n", "") for requirement in requirement_file
            ]
            requirement_list.remove(REMOVE_PACKAGE)
        return requirement_list
    except Exception as e:
        raise e


setup(
    name=SRC_REPO,
    license=__license__,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    # description="A small python package for CNN app",
    # url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    # project_urls={
    #     "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    # },
    # package_dir={"": "src"},
    packages=find_packages(),
    install_requires=get_requirement_list(),
)
