# paas_manager
API server that does simple resource, access and quota management.

Steps to use the API:

1) Use the make file to test and run the api server.(Make sure you have python3 installed on the host)
2) After you start the api, create a superuser/admin using "python3 manage.py createsuperuser"
3) api context is /api/v1 so the local url will be "localhost:8000/api/v1/"
4) You will see two end points there for users and resources
5) Only admin user can use the user endpoint (create/update/delete users)
6) All the normal users can login and create/modify/delete their resources based on thier qouta
7) Admin user can create/modify/delete anyone's resources