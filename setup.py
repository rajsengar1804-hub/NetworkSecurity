from setuptools import find_packages,setup
from typing import List
def get_requirements()->List[str]:
    requirements_list:List[str] =[]
    try :
        with open("requirements.txt",'r') as file :
            lines =file.readlines()
            for line in lines :
                 requirement=line.strip()
                 if requirement and requirement !='-e .':
                     requirements_list.append(requirement)
                     
    except Exception as ex :
        print(ex)
    return requirements_list
setup(
name="Network Security",
version="0.0.1",
author="Raj Pratap Singh Sengar",
author_email="rajsengar1804@gmail.com",
packages=find_packages(),
install_requires=get_requirements()
)
        