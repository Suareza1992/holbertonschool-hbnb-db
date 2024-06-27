HBnB Evolution: Part 2 (Database Persistence)

Concepts
For this project, we expect you to look at this concept:

Databases
Database Integration and Security Enhancements for HBnB Evolution Project
In Part 2 of the HBnB Evolution project, you will enhance your application by integrating a relational database using SQLAlchemy, an Object-Relational Mapper (ORM), and by implementing security measures through JWT authentication. This phase aims to provide students with a real-world experience of upgrading an existing application to support more scalable and secure operations.

Learning Objectives

Understand and Implement ORM: Students will learn how to integrate SQLAlchemy into a Flask application to handle database operations seamlessly.
Database Management: Gain experience in configuring and managing a relational database, including schema design and migrations.
Security Implementation: Learn to secure API endpoints using JWT authentication, ensuring that data access is regulated and secure.
Adaptability and Scalability: Enhance the application’s adaptability by allowing dynamic switching between different persistence methods and preparing for scalable deployment.
Tasks to be Accomplished

Integrating SQLAlchemy:

Modify the application to include SQLAlchemy, setting up models to interact with a database while keeping the option for file-based persistence.
Ensure that all models are correctly transformed into SQLAlchemy ORM-compatible classes.
Configure SQLAlchemy to connect to a SQLite database for development purposes.
Configurable Database Selection:

Implement a configuration system that allows the application to toggle between using SQLite for development and a more robust database like PostgreSQL for production.
Ensure the application can dynamically choose the database type based on environment settings or configuration files.
Implementing Authentication with JWT:

Integrate Flask-JWT-Extended to add secure authentication mechanisms to the API.
Create endpoints for user authentication that issue JWTs and use these tokens to control access to various API endpoints.
Database Schema Design and Migration:

Design a database schema that accurately represents the data relationships and business rules.
Create the SQL scripts for your database structure. Optionally, use tools like Alembic to manage database migrations.
Role-Based Access Control:

Modify existing API endpoints to incorporate checks for user roles and permissions, restricting certain actions to authenticated users or administrators.
Docker Integration:

Update the Docker configuration to support the new database and authentication functionalities.
Ensure that the Docker environment is configured to handle different database types and authentication services.
Resources:

SQLAlchemy Documentation: Utilize the SQLAlchemy docs to understand ORM configuration and usage.
Flask-JWT-Extended Tutorial: Refer to resources on Flask-JWT-Extended to learn how to implement JWT in Flask applications.
Alembic for Migrations: Check out Alembic documentation for guidance on database migrations.
Environment Configuration: Use environment variables to manage database connections and other settings, ensuring flexibility across different deployment environments.
Security Best Practices: Learn about security best practices, particularly in storing passwords securely and managing user authentication.
As an enhancement to this part of the HBnB Evolution project, it’s crucial to integrate real-world database testing into your application development. Therefore, you will use a Docker container with MySQL or PostgreSQL as an external server to test their implementation.

Instructions for Using Docker with MySQL/PostgreSQL

Choose a Database: Decide whether you want to use MySQL or PostgreSQL for your production database.

Pull the Docker Image:

For MySQL: docker pull mysql
For PostgreSQL: docker pull postgres
Run the Database in a Docker Container:

For MySQL: docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
For PostgreSQL: docker run --name postgres-db -e POSTGRES_PASSWORD=my-secret-pw -d postgres Replace my-secret-pw with a secure password.
Configure Your Application:

Update your application’s configuration to connect to the database running in the Docker container.
Use the appropriate connection string for MySQL or PostgreSQL.
Test Your Application:

Ensure your application correctly connects to and interacts with the database within the Docker container.
Conduct all relevant tests to verify database operations.
Resources for Setup and Testing

Docker Official Documentation: Get Started with Docker
MySQL Docker Image Documentation: MySQL Docker Official Image
PostgreSQL Docker Image Documentation: PostgreSQL Docker Official Image
Connecting to MySQL/PostgreSQL from Python: Look into SQLAlchemy documentation for MySQL and PostgreSQL.
Tasks
0. Integrating SQLAlchemy
mandatory
This task involves integrating SQLAlchemy into your HBnB Evolution project, enabling a transition from your current data management system to a robust database-backed system using an ORM (Object-Relational Mapper). Given the flexibility suggested by the DataManager pattern used earlier, this task will build upon that architecture to incorporate SQLAlchemy effectively.

Objectives

Integrate SQLAlchemy ORM into the Flask application, leveraging the existing DataManager structure.
Adapt current data models to work as SQLAlchemy ORM classes while maintaining compatibility with the DataManager interface.
Ensure the application can dynamically switch between the existing file-based system and the new database-backed system based on configuration.
Requirements

SQLAlchemy Integration: Incorporate SQLAlchemy to manage database interactions.
Model Adaptation: Convert existing models to use SQLAlchemy’s ORM features, including the newly added fields (password and is_admin) needed for authentication and authorization.
Flexible Persistence Switching: Enable seamless switching between file-based and database persistence modes using environment configuration.
Instructions

Update Project Dependencies:

Ensure SQLAlchemy and Flask-SQLAlchemy are included in your project dependencies. Add these to your requirements.txt to manage installations efficiently.
Initialize SQLAlchemy in Your Flask Application:

Configure your Flask app to use SQLAlchemy, initially connecting to a SQLite database for development purposes.
Example configuration:
 from flask_sqlalchemy import SQLAlchemy

 app = Flask(__name__)
 app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
 db = SQLAlchemy(app)
Refactor Existing Models to Extend SQLAlchemy:

Modify your data models to extend from db.Model, SQLAlchemy’s declarative base, ensuring they implement the methods defined by your DataManager interface.
Define attributes using SQLAlchemy’s column types and relationships.
Example for a User model:
 class User(db.Model):
     id = db.Column(db.String(36), primary_key=True)
     email = db.Column(db.String(120), unique=True, nullable=False)
     password = db.Column(db.String(128), nullable=False)  # Ensure secure storage
     is_admin = db.Column(db.Boolean, default=False)
     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
     updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
Enhance DataManager to Handle Both Persistence Types:

Adjust the DataManager to manage both file-based and database interactions, possibly using an environment variable to switch between the modes.
Implement conditional logic within the DataManager methods to direct queries to the appropriate storage type based on the configuration.
Example of conditional persistence logic:
 class DataManager:
     def save_user(self, user):
         if app.config['USE_DATABASE']:
             db.session.add(user)
             db.session.commit()
         else:
             # Implement file-based save logic
             pass
Testing and Validation:

Develop comprehensive tests to ensure that both the database interactions via SQLAlchemy and the fallback to file-based operations function as expected.
Test CRUD operations, relationship management, and the dynamic switching mechanism to verify full system integrity.
Resources

SQLAlchemy Documentation
Flask-SQLAlchemy Extension
SQL Database Design Basics
Repo:

GitHub repository: holbertonschool-hbnb-db
0/0 pts
1. Configurable Database Selection
mandatory
In this task, you will implement a flexible database configuration system for the HBnB Evolution project. This system will enable the application to seamlessly switch between different database environments using SQLite for development and a more robust database like PostgreSQL for production. The goal is to ensure that the application can adapt to different environments without requiring code changes, facilitating easier testing and deployment.

Objectives

Develop a dynamic database configuration system that allows switching between SQLite and PostgreSQL based on environment settings.
Ensure the application initializes the correct database type at startup and connects successfully.
Implement functionality to support easy transition and configuration for different deployment scenarios.
Requirements

Flexible Database Configuration: Implement a system that uses environment variables or configuration files to select the appropriate database at startup.
Database Initialization: Ensure that the SQLite database is automatically created if it does not exist when the application is run in development mode.
Connection Details for Production Database: Set up and test connection parameters for a PostgreSQL database when in production mode.
Instructions

Environment Setup:

Define environment variables that specify the database type (SQLite for development and PostgreSQL for production). These variables should be easily configurable, e.g., through a .env file or a configuration module within the application.
Example environment variables:
 DATABASE_TYPE=sqlite  # Options: 'sqlite', 'postgresql'
 DATABASE_URL=sqlite:///dev.db  # URL for SQLite or connection string for PostgreSQL
Database Configuration in Application:

Modify the application configuration to dynamically set the database connection based on the environment variables.
Use a configuration class or a similar approach to manage different settings for development, testing, and production environments.
Example configuration setup in Flask:
 class Config(object):
     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

 class DevelopmentConfig(Config):
     DEBUG = True

 class ProductionConfig(Config):
     DEBUG = False

 app.config.from_object('config.DevelopmentConfig' if os.environ.get('ENV') == 'development' else 'config.ProductionConfig')
 db = SQLAlchemy(app)
Database Initialization for Development:

Implement logic to check if the SQLite database exists and create it if it does not. This step is crucial to ensure a smooth development experience.
Ensure that SQLAlchemy is configured to handle this initialization automatically where possible, or write scripts to set up the database initially.
Testing Connection and Transitions:

Write tests to verify that the application correctly determines which database to connect to based on the environment settings.
Test the application’s ability to connect to both SQLite and PostgreSQL databases and perform basic CRUD operations to validate the connections.
Ensure that switching from one database type to another does not require changes in the business logic of the application.
Resources

SQLAlchemy Engine Configuration: SQLAlchemy Engine Configuration
Environment Variables in Python: Python Documentation on os.environ
Database Security Best Practices: Database Security Best Practices
Repo:

GitHub repository: holbertonschool-hbnb-db
0/1 pt
2. Implementing Authentication with JWT
mandatory
In this task, you will integrate JSON Web Token (JWT) authentication into the HBnB Evolution project using the Flask-JWT-Extended plugin. This integration aims to secure API endpoints by verifying user credentials and providing tokens for authenticated sessions. You will also enhance user management by adding password handling and administrative flags to the user model.

Objectives

Implement JWT-based authentication to secure API endpoints.
Create a login endpoint to validate user credentials and issue JWTs.
Update the User model to include password storage using best practices for security and a boolean flag to denote administrative status.
Ensure only authenticated users can access protected endpoints, with additional checks for administrative privileges where necessary.
Requirements

JWT Integration: Add JWT authentication capabilities to the Flask application.
Secure Password Handling: Implement secure password storage and verification.
Role-Based Access Control: Modify API endpoints to require authentication and, in some cases, administrative privileges.
User Model Updates: Enhance the User model to support authentication and role checks.
Instructions

Set Up JWT Authentication:

Install Flask-JWT-Extended and add it to your project dependencies.
Configure JWT in your Flask application, setting up secret keys and any relevant JWT properties.
Example configuration:
 from flask_jwt_extended import JWTManager

 app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
 jwt = JWTManager(app)
Create a Login Endpoint:

Develop a login endpoint that authenticates users based on their email and password.
Upon successful authentication, issue a JWT that will be used to access protected endpoints.
Example login endpoint:
 @app.route('/login', methods=['POST'])
 def login():
     username = request.json.get('username', None)
     password = request.json.get('password', None)
     user = User.query.filter_by(username=username).first()
     if user and bcrypt.check_password_hash(user.password, password):
         access_token = create_access_token(identity=username)
         return jsonify(access_token=access_token), 200
     return 'Wrong username or password', 401
Modify User Model for Authentication:

Update the User model to include a password field and an is_admin field. Use bcrypt to hash passwords before storing them in the database. (Why?)
Example User model update:
 from flask_bcrypt import Bcrypt

 bcrypt = Bcrypt(app)

 class User(db.Model):
     # existing fields...
     password_hash = db.Column(db.String(128))
     is_admin = db.Column(db.Boolean, default=False)

     def set_password(self, password):
         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

     def check_password(self, password):
         return bcrypt.check_password_hash(self.password_hash, password)
Secure API Endpoints:

Update API endpoints to require a valid JWT for access. Use Flask-JWT-Extended decorators to handle these requirements.
Implement additional checks for endpoints that require administrative privileges.
Example of securing an endpoint:
 from flask_jwt_extended import jwt_required, get_jwt_identity

 @app.route('/protected', methods=['GET'])
 @jwt_required()
 def protected():
     current_user = get_jwt_identity()
     return jsonify(logged_in_as=current_user), 200
Testing and Validation:

Develop tests to ensure that the login process works correctly and that JWTs are issued as expected.
Test protected endpoints to verify that they correctly authenticate access based on the provided JWT.
Ensure that administrative endpoints are only accessible to users with the appropriate privileges.
Repo:

GitHub repository: holbertonschool-hbnb-db
0/ pts
3. Database Schema Design and Migration
mandatory
In this task, you will design a comprehensive database schema for the HBnB Evolution project and create the necessary SQL scripts to initialize the database. You will also implement optional migration scripts using Alembic to manage changes to the database structure over time. This ensures the scalability and maintenance of the application as it evolves.

Objectives

Create a detailed database schema diagram reflecting the relationships and structures decided in the UML design phase.
Write SQL scripts to create the database, tables, and initial data.
Optionally, implement database migration scripts using Alembic to handle the creation and updates of database schemas.
Ensure the application can handle schema changes without data loss and with minimal downtime.
Requirements

Database Schema Diagram: Develop a visual representation of the database schema including tables, relationships, primary keys (PKs), and foreign keys (FKs).
SQL Scripts: Write scripts that allow for the creation, modification, and initialization of database tables and relationships.
Optional Alembic Integration: Integrate Alembic into the project for managing migrations effectively.
Instructions

Designing the Database Schema:

Translate the UML class diagrams into a relational database schema. This includes defining tables for each entity, their relationships, and ensuring that foreign key constraints are correctly implemented.
Use a database design tool to create a visual schema diagram. This diagram should be included in the project documentation for reference.
Example tools include Lucidchart, dbdiagram.io, or ERBuilder.
Writing SQL Scripts:

Write SQL scripts to create the database and tables based on the schema you designed. Include statements to define primary keys, foreign keys, and any necessary constraints.
Ensure that the scripts also insert initial data into the tables, such as default values or test data.
Example SQL script for creating a User table:
 CREATE TABLE User (
     id VARCHAR(36) PRIMARY KEY,
     email VARCHAR(120) UNIQUE NOT NULL,
     password VARCHAR(128) NOT NULL,
     is_admin BOOLEAN DEFAULT FALSE,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
 );
Setting Up Alembic for Optional Migrations:

Install Alembic and configure it within your Flask application.
Initialize Alembic in the project directory to create the necessary configuration files and migration environment.
Example setup: bash alembic init migrations
Modify the alembic.ini file and the env.py within the migrations folder to connect to your project’s database using SQLAlchemy.
Creating and Managing Migrations (Optional):

Write your first migration script using Alembic to create initial database tables based on your SQLAlchemy models.
Use Alembic commands to generate migration scripts automatically whenever you modify the models.
Manually review and adjust the auto-generated scripts to ensure accuracy and efficiency.
Example command to create a migration after model changes: bash alembic revision --autogenerate -m "Added user table"
Apply migrations to update the database schema: bash alembic upgrade head
Testing Migrations:

Test your SQL scripts and migration scripts (if using Alembic) in both development (using SQLite) and production-like environments (using PostgreSQL) to ensure they execute without errors.
Verify that schema changes are applied correctly and that no data is lost during migrations.
Include rollback procedures in your tests to ensure that you can revert to previous states if a migration fails.
Resources

SQLAlchemy Documentation
Flask-SQLAlchemy Extension
Alembic Documentation
SQL Database Design Basics
Lucidchart
dbdiagram.io
Repo:

GitHub repository: holbertonschool-hbnb-db
0/ pts
4. Implementing Role-Based Access Control
mandatory
In this task, you will enhance the security of the HBnB Evolution project by implementing role-based access control (RBAC) within the application. This involves modifying existing API endpoints to restrict certain actions based on the user’s role, ensuring that only authorized users can access specific functionalities.

Objectives

Integrate role-based access controls into the application to manage user permissions effectively.
Modify API endpoints to differentiate access between normal users and administrators.
Secure endpoints so that actions such as creating, updating, or deleting resources are appropriately restricted.
Requirements

Role Identification: Ensure the User model includes an is_admin boolean attribute to identify administrative users.
Protected Endpoints: Update API endpoints to check user roles before allowing modifications to resources.
JWT Role Checks: Utilize JWTs to carry role information and enforce access controls based on these roles.
Instructions

Update User Authentication:

Modify the login process to include role information in the JWT. This will allow the application to make role-based decisions without needing to query the database repeatedly for the user’s role.
Example of adding role to JWT claims: “`python from flaskjwtextended import createaccesstoken
def login(): # authenticate user additionalclaims = {"isadmin”: user.isadmin} accesstoken = createaccesstoken(identity=user.id, additionalclaims=additionalclaims) return jsonify(accesstoken=accesstoken) “`

Securing API Endpoints:

Implement checks in API endpoints to ensure that users can only access data according to their roles. For example, restrict endpoints that manage amenities and cities to administrators only.
Example of a protected endpoint: ”`python from flaskjwtextended import jwtrequired, getjwtidentity, getjwt
@app.route(‘/admin/data’, methods=[‘POST’, ‘DELETE’]) @jwtrequired() def admindata(): claims = getjwt() if not claims.get(‘isadmin’): return jsonify({“msg”: “Administration rights required”}), 403 # Proceed with admin-only functionality “`

Endpoint Access Breakdown:

Public Endpoints:

User Login: POST /login
View Places: GET /places
View Place Details: GET /places/<place_id>

** Authenticated Endpoints **:

Submit Reviews: POST /places/<place_id>/reviews

Edit Reviews: PUT /places/<place_id>/reviews (Only for those reviews created by the user)

Manage Places: POST /places, PUT /places/<place_id>, DELETE /places/<place_id> (Only for those places OWNED by the user)

Protected Admin Endpoints (administrative access required): - Manage Amenities: POST /amenities, DELETE /amenities/<amenity_id> - Manage Cities: POST /cities, DELETE /cities/<city_id> - Manage Places: POST /places, PUT /places/<place_id>, DELETE /places/<place_id> - Manage Users: POST /users, PUT /users/<user_id>, DELETE /users/<user_id>

> This is not an exhaustive list. You should review all the actions and evaluate the need of authentication and level of authorization required.
Testing Role-Based Access Control:

Write tests to verify that each endpoint respects the role-based access rules.
Include tests for both authorized and unauthorized access to ensure the security measures are effective and correctly implemented.
User Role Management:

Implement functionality to allow administrators to change the role of users, such as promoting a normal user to an administrator.
Ensure changes to user roles are appropriately reflected in subsequent API calls, requiring re-authentication if necessary.
Status Codes for Authentication and Authorization

200 OK: Request was successful. Example: Successfully accessed a public or protected endpoint with appropriate permissions.

401 Unauthorized: Authentication is required and has failed or has not yet been provided. Example: Attempting to access an endpoint without a valid JWT token.

403 Forbidden: The server understood the request but refuses to authorize it. This happens when a user does not have the necessary permissions. Example: A non-admin user attempting to access an admin-only endpoint.

400 Bad Request: The server could not understand the request due to invalid syntax. Example: Malformed request or invalid input data in the request payload.

Repo:

GitHub repository: holbertonschool-hbnb-db
0/ pts
5. Updating Docker Configuration
mandatory
In this final task of Part 2 of the HBnB Evolution project, you’ll update and optimize the Docker configuration to include the new version of the API with database support, SQLAlchemy integration, and JWT authentication. This step is crucial to ensure that your application can be easily deployed in various environments, maintaining consistency and reliability across development, testing, and production settings.

Objectives

Update the Dockerfile to include all necessary components for the newly integrated database and authentication functionalities.
Ensure the Docker environment is properly configured to handle different database types and authentication mechanisms.
Optimize the Docker build process for efficiency and security.
Requirements

Updated Dockerfile: Modify the existing Dockerfile to support SQLAlchemy and the necessary environment for both SQLite and PostgreSQL databases.
Environment Configuration: Configure environment variables in Docker to manage database connections and JWT settings effectively.
Security Enhancements: Include security practices in the Docker setup to protect sensitive data and minimize potential vulnerabilities.
Instructions

Revise the Dockerfile:

Ensure that the Dockerfile installs all required dependencies for SQLAlchemy and supports both SQLite for development and PostgreSQL for production.
Update the base image if necessary to support the latest Python and Flask versions.
Example Dockerfile modifications: dockerfile FROM python:3.8-alpine RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev COPY . /app WORKDIR /app RUN pip install -r requirements.txt EXPOSE 5000 CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
Configure Environment Variables:

Use a .env file or Docker secrets to manage sensitive information such as database credentials and JWT secret keys securely.
Ensure these variables are accessible within your application at runtime.
Example of setting environment variables in Docker-compose: yaml version: '3.8' services: web: build: . ports: - "5000:5000" environment: - DATABASE_URL=postgresql:///prod_db - JWT_SECRET_KEY=your_secret_key volumes: - .:/app
Optimize Docker Build and Setup:

Optimize the Docker build process by properly ordering Dockerfile commands to maximize layer caching.
Minimize the Docker image size by cleaning up unnecessary files and dependencies after installation.
Ensure that the Docker setup includes proper logging and monitoring capabilities to facilitate debugging and performance tracking in production environments.
Testing and Validation:

Test the Docker build process to ensure it completes without errors and results in a functional application environment.
Perform end-to-end tests to confirm that the application behaves as expected within the Docker container, including database interactions and JWT authentication processes.
Validate the security configurations by checking for potential leaks of sensitive information and ensuring that no unnecessary ports are exposed.
Repo:

GitHub repository: holbertonschool-hbnb-db

Authors:

Ángel Suárez (Suareza1992)(7630@holbertonstudents.com)
