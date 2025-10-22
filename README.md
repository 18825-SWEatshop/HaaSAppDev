
# HaaSAppDev  

Hardware-as-a-Service project for ECE461L

## Requirements
- **Python 3.9+** 
- **uv installed**  

You can install uv using pip:
```pip install uv ``` and verify installation with ```uv --version```

## Setup
- Clone the repository 
  - ```git clone git@github.com:18825-SWEatshop/HaaSAppDev.git```
- UV setup 
  - ```uv sync```
- .env setup 
  - ```add the .env file shared in the team chat```
- Start FastAPI Dev server
  - ```uv run fastapi dev```
  - By default, the server will be available at ```127.0.0.1:8000```

## For Developers 
- To add a new dependency to the project:
  - ```uv add <package-name>```
- To remove a dependency from the project:
  - ```uv remove <package-name>```
- To upgrade dependencies:
  - ```uv update```
