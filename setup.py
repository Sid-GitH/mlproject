from setuptools import find_packages, setup    # automatically finds out all packages in the whole code
from typing import List

hypen_e_dot = '-e .'     # connector from requirements.txt - should be removed

def get_requirements(file_path:str) -> List[str]:
   '''
    Function returns a list of string from the requirements.txt

    '''
   requirements=[]
   with open(file_path) as file_obj:
      requirements = file_obj.readlines()
      requirements = [requirement.replace('\n',"") for requirement in requirements]
      if hypen_e_dot in requirements:
         requirements.remove(hypen_e_dot) 
      return requirements

      


setup(
name='mlproject',
version='0.0.1',
author = 'Sid',
author_email= 'siddharthbala.5@gmail.com',
packages=find_packages(),
install_requires = get_requirements('requirements.txt')                                      #['pandas','numpy', 'seaborn']
)