#project setup
* app: contains a fastapi webapp


# App
## Design 
* We use the controller, service, repository pattern, except for the health endpoint. Each layer gets a folder for each feature.
* we use entities (business logic models) and schemas (API request / response models). entities are stored in the service folder and the schemas in the controller folder. schemas have a from_entitiy or to_entitiy method if needed.
* use fastapi dependnecy resolution (e.g. my_service = Dapends(MyService))


# General rules: 
* never install anything. Instead ask the user to install it and how, and then continue.
* Before generating anything, ask the user for clarifying questions if needed and generate 3 options too choose from.