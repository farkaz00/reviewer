# Reviewer
This is a simple Django backend to allow users to submit their reviews to any company registered in the system. It uses a simple `sqlite` database to store the data to ease deployment and taking backups.

## Installation and Deployment
This application requires `python 3.5.3` or greater and `pip`.

Once the repository has been downloaded, create a python virtual environment and run `pip install -r requirements.txt`.

Create a *super user* by running `python manage.py createsuperuser`.

Run the required migrations by executing `python manage.py migrate`.

Run the tests by executing `python manage.py test`. Although it lists *models.py* they don't require tests since they are plain `django models`.

Run the application by executing `python manage.py runserver`. The server will run on the default route `http://localhost:8000/`.

## API Description
The API exposes three endpoints which are described as follows.

### Login
This endpoint is used to obtain an *authorization token* to be allowed to use the rest of the endpoints in the application.

*Default Endpoint*: `http://localhost:8000/reviews_v1/login`
#### Login Operation: 

*Request*: POST `http://localhost:8000/reviews_v1/login`

*Form Data*:
  * username: registered User's username.
  * password: registered User's password.

*Sample Output*

```javascript
{
    "token": "7d28ce1df60ef118186171426c941e815ca5f17a"
}
```


### Users
Users must supply an *authorization token* in the *Authorization* field from the  request header to access this endpoint.

This endpoint is used to list and create additional users into the system. It can only be accessed by `staff` users.

*Default Endpoint*: `http://localhost:8000/reviews_v1/users`

#### List Operation
*Endpoint* GET `http://localhost:8000/reviews_v1/users`

*Sample output*

```javascript
[
    {
        "first_name": "",
        "last_name": "",
        "username": "admin",
        "password": "pbkdf2_sha256$120000$OJdCTWVVHp1B$nyHfYtFtYSzBOlDtNnlSdwjBt3TTXoOq1a63MDdcVMk=",
        "email": "",
        "is_staff": true
    },
    {
        "first_name": "John",
        "last_name": "Doe",
        "username": "jhon",
        "password": "pbkdf2_sha256$120000$PtgVJEuK53Ce$fL/iwBn9pwLcm1LU72oG9Ju4VJB1VnRK/pPMRRTEJc4=",
        "email": "john@doe.com",
        "is_staff": false
    }
]
```

#### Create Operation
*Request*: POST `http://localhost:8000/reviews_v1/users`

*Body*

```javascript
{
    "first_name": "John",
    "last_name": "Doe",
    "username": "jhon",
    "password": "pass",
    "email":"john@doe.com",
    "is_staff": "false"
}
```

### Companies
Users must supply an *authorization token* in the *Authorization* field from the  request header to access this endpoint.

This endpoint is used to list and create additional companies into the system to be reviewed by users.

*Default Endpoint*: `http://localhost:8000/reviews_v1/companies`

#### List Operation
*Endpoint* GET `http://localhost:8000/reviews_v1/companies`

*Sample output*

```javascript
[
    {
        "id": 1,
        "name": "Company1"
    },
    {
        "id": 2,
        "name": "Company2"
    }
]
```

#### Create Operation
*Request*: POST `http://localhost:8000/reviews_v1/companies`

*Body*

```javascript
{
    "name": "Company1",
}
```

### Reviews
Users must supply an *authorization token* in the *Authorization* field from the  request header to access this endpoint.

This endpoint is used to list and create additional reviews into the system. Users can only list their own reviews. However, staff users can list all reviews in the system, regardless of them being the review's author or not.

*Default Endpoint*: `http://localhost:8000/reviews_v1/reviews`

#### List Operation
*Endpoint* GET `http://localhost:8000/reviews_v1/reviews`

*Sample non admin output*

```javascript
[
    {
        "company": 1,
        "reviewer": 2,
        "title": "Review by John",
        "summary": "This is a review posted by user john",
        "rating": 5,
        "ip_address": "192.168.1.1"
    }
]
```

*Sample admin output*

```javascript
[
    {
        "company": 1,
        "reviewer": 1,
        "title": "Admin review",
        "summary": "This is a review posted by an admin",
        "rating": 5,
        "ip_address": "192.168.1.1"
    },
    {
        "company": 1,
        "reviewer": 2,
        "title": "Review by John",
        "summary": "This is a review posted by user john",
        "rating": 5,
        "ip_address": "192.168.1.1"
    }
]
```

#### Create Operation
*Request*: POST `http://localhost:8000/reviews_v1/companies`

*Body*

```javascript
{
    "company": 1,
    "reviewer": 1,
    "title": "Admin review",
    "summary": "This is a review posted by an admin",
    "rating": 5,
    "ip_address": "192.168.1.1"
}
```
