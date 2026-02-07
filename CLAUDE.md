#project setup
* app: contains a fastapi webapp

# App
## Design
* We use the controller, service, repository pattern, except for the health endpoint. Each layer gets a folder for each feature.
* we use entities (business logic models) and schemas (API request / response models). entities are stored in the service folder and the schemas in the controller folder. schemas always have a from_entity class method for conversion.
* use fastapi dependency resolution (e.g. my_service = Dapends(MyService)) when possible over getter methods.
* use pydantic-settings to handle global app settings including database provisioning.
* we use sqlalchemy to handle sql queries. we use ORM models and avoid plain sql where possible.
* never use raw tuples or unstructured types (e.g. `tuple[list[X], int]`) as return types. use a proper model or entity instead.
* list endpoints must always return a paginated response (items, total, page, page_size). use a generic `PaginatedResponse[T]` / `PaginatedResult[T]` — do not create per-type paginated classes.
* when a repository needs to return both items and a count, combine them into a single method to avoid race conditions between separate queries.
* prefer generic types over duplicating similar classes. ad-hoc specialization (e.g. `PaginatedResponse[MyModel]`) in the controller is fine — no need for dedicated type aliases in schemas.

# General rules:
* do not generate docstrings unless there is important information about a function to be put in it.
* never install anything. Instead ask the user to install it and how, and then continue.
* Before generating anything, ask the user for clarifying questions if needed and generate 3 options too choose from.
* never use comments to separate a file into sections. if this is needed the file is too big and should be split into smaller files.
* keep fixtures at the lowest level possible until they need to be re-used. if you add a fixture search the code if it exists already on a lower level.

# Testing rules:
* use `# given`, `# when`, `# then` comments to structure every test. use `# when / then` when they are inseparable (e.g. pytest.raises).
* one test file per layer: `test_<feature>_service.py`, `test_<feature>_endpoint.py`.
* one test class per method/endpoint being tested. class name reflects the method (e.g. `TestAddTask`, `TestGetAllRepeatingTasks`).
* integration tests must never call other endpoints to set up data. use seed fixtures that insert directly via the db session.
* always cover both the happy path and the primary error path (e.g. 404 for missing resource, validation rejection).
