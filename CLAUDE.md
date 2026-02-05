#project setup
* app: contains a fastapi webapp

# App
## Design 
* We use the controller, service, repository pattern, except for the health endpoint. Each layer gets a folder for each feature.
* we use entities (business logic models) and schemas (API request / response models). entities are stored in the service folder and the schemas in the controller folder. schemas have a from_entitiy or to_entitiy method if needed.
* use fastapi dependnecy resolution (e.g. my_service = Dapends(MyService)) when possible over getter methds.
* use pydantic-settings to handle global app settings including database provisioning.
* we use sqlalchemy to handle sql queries. we use ORM models and avoid plain sql where possible.

# General rules: 
* do not generate docstrings unless there is important information about a function to be put in it.
* never install anything. Instead ask the user to install it and how, and then continue.
* Before generating anything, ask the user for clarifying questions if needed and generate 3 options too choose from.
* never use comments to separte a file into sections. if this is needed the file is too big and should be split into smaller files.
* keep fixtures at the lowest level possible until they need to be re-used. if you add a fixture search the code if it exists already on a lower level.