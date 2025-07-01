from setuptools import find_packages, setup
from typing import List


def get_requirements() -> List[str]:
    """
    This function will return the list of requirements
    """
    requirement_list: List[str] = []

    try:
        # open and read the requirements.txt file
        with open("requirements.txt", "r") as file:
            # Read lines from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                # Strip whitespace and newline characters
                requirement = line.strip()
                # Ignore empty lines, comments, and editable installs
                if (
                    requirement
                    and not requirement.startswith("#")
                    and not requirement.startswith("-e")
                ):
                    requirement_list.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found.")

    return requirement_list


setup(
    name="ai-trip-planner",
    version="0.0.1",
    author="Abhishek Kumar",
    author_email="abhishek@genailytics.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
