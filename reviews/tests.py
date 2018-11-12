import json

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import (APITestCase, APIRequestFactory,
        force_authenticate)

from .models import Company, Review

from .views import login, UserListCreate, CompanyListCreate, ReviewListCreate

USER_USERNAME = 'jhon'
USER_PASSWORD = 'pass'
USER_FIRST_NAME = 'John'
USER_LAST_NAME = 'Doe'
USER_EMAIL = 'john@doe.com'
USER_IS_STAFF = False

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'
ADMIN_FIRST_NAME = 'Administrator'
ADMIN_LAST_NAME = ''
ADMIN_EMAIL = 'admin@corp.com'
ADMIN_IS_STAFF = True

def createUsers():
    User.objects.create_user(\
            username=USER_USERNAME,\
            password=USER_PASSWORD,\
            first_name=USER_FIRST_NAME,\
            last_name=USER_LAST_NAME,\
            email=USER_EMAIL,\
            is_staff=USER_IS_STAFF)

    User.objects.create_superuser(\
            username=ADMIN_USERNAME,\
            password=ADMIN_PASSWORD,\
            first_name=ADMIN_FIRST_NAME,\
            last_name=ADMIN_LAST_NAME,\
            email=ADMIN_EMAIL,\
            is_staff=ADMIN_IS_STAFF)

def getToken(username, password):
        factory = APIRequestFactory()
        request = factory.post('/reviews_v1/login', \
                {'username':username, 'password':password})
        response = login(request)
        return response.data.get('token')

def clearUsers():
    User.objects.all().delete()


class LoginTestCase(APITestCase):

    def setUp(self):
        createUsers()

    def tearDown(self):
        clearUsers() 

    def test_successful_login(self):
        user_token = getToken(USER_USERNAME, USER_PASSWORD)
        token = Token.objects.get(user__username=USER_USERNAME)
        self.assertEqual(token.key, user_token)

    def test_bad_request_login(self):
        user = User.objects.get(username=USER_USERNAME)
        factory = APIRequestFactory()
        request = factory.post(\
                '/reviews_v1/login', \
                {'username':user.username})
        response = login(request)
        self.assertEqual(400, response.status_code)

    def test_not_found_login(self):
        factory = APIRequestFactory()
        request = factory.post(\
                '/reviews_v1/login', \
                {'username':'yakirish', 'password':'makirish'})
        response = login(request)
        self.assertEqual(404, response.status_code)


class UserTestCase(APITestCase):
    def setUp(self):
        createUsers()

    def tearDown(self):
        clearUsers()

    def test_successful_user_create(self): 
        user_count_init = User.objects.all().count()
        factory = APIRequestFactory()
        token = getToken(ADMIN_USERNAME, ADMIN_PASSWORD)
        user = User.objects.get(username=ADMIN_USERNAME)
        request = factory.post('/reviews_v1/users',\
                json.dumps({\
                    'first_name': 'Jane',\
                    'last_name': 'Doe',\
                    'username': 'jane',\
                    'password': 'pass',\
                    'email':'jane@doe.com',\
                    'is_staff': 'false'\
                    }),\
                content_type='application/json')
        force_authenticate(request, user=user, token=token)
        view = UserListCreate.as_view()
        response = view(request)
        user_count_final = User.objects.all().count()
        self.assertEqual(201, response.status_code)
        self.assertEqual(user_count_init+1, user_count_final)

    def test_bad_request_user_create(self): 
        user_count_init = User.objects.all().count()
        factory = APIRequestFactory()
        token = getToken(ADMIN_USERNAME, ADMIN_PASSWORD)
        user = User.objects.get(username=ADMIN_USERNAME)
        request = factory.post('/reviews_v1/users',\
                json.dumps({\
                    'first_name': 'Jane',\
                    'last_name': 3,\
                    'username': '{jane}',\
                    'password': 'pass',\
                    'email':'jane@doe.com',\
                    'is_staff': 'false'\
                    }),\
                content_type='application/json')
        force_authenticate(request, user=user, token=token)
        view = UserListCreate.as_view()
        response = view(request)
        user_count_final = User.objects.all().count()
        self.assertEqual(400, response.status_code)
        self.assertEqual(user_count_init, user_count_final)


#class CompanyTestCase(APITestCase):

#    def setUp(self):
#        createUsers()
#        self.company1 = Company()
#        self.company1.name='Company1'
#        self.company1.save()

#    def tearDown(self):
#        clearUsers()
#        Company.objects.all().delete()

#    def test_list_companies(self):
#        factory = APIRequestFactory()
#        token = getToken(USER_USERNAME, USER_PASSWORD)
#        user = User.objects.get(username=USER_USERNAME)
#        request = factory.get('/reviews_v1/companies')
#        force_authenticate(request, user=user, token=token)
#        view = CompanyListCreate.as_view()
#        response = view(request)
#        print(response.data)
#        self.assertEquals(len(response.data), 1)
#        self.assertEquals(response.data[0]['id'], self.company1.id)
#        self.assertEquals(response.data[0]['name'], self.company1.name)

#    def test_successful_company_create(self):
#        company_count_init = Company.objects.all().count()
#        factory = APIRequestFactory()
#        token = getToken(ADMIN_USERNAME, ADMIN_PASSWORD)
#        user = User.objects.get(username=ADMIN_USERNAME)
#        request = factory.post('/reviews_v1/companies',\
#                json.dumps({'name':'Company2'}),\
#                content_type='application/json')
#        force_authenticate(request, user=user, token=token)
#        view = CompanyListCreate.as_view()
#        response = view(request)
#        company_count_final = Company.objects.all().count()
#        self.assertEqual(201, response.status_code)
#        self.assertEqual(company_count_init+1, company_count_final)


class ReviewTestCase(APITestCase):

    def setUp(self):
        createUsers()
        user = User.objects.get(username=USER_USERNAME)
        admin_user = User.objects.get(username=ADMIN_USERNAME)
        self.company1 = Company()
        self.company1.name='Company1'
        self.company1.save()
        self.company2 = Company()
        self.company2.name='Company2' 
        self.company2.save()
        Review.objects.all().delete()
        self.user_review = Review()
        self.user_review.title = 'Review by user'
        self.user_review.summary = 'This is a review by user'
        self.user_review.rating = 3
        self.user_review.ip_address = '192.168.1.2'
        self.user_review.reviewer = user
        self.user_review.company = self.company1
        self.user_review.save()
        self.admin_review = Review()
        self.admin_review.title = 'Review by admin'
        self.admin_review.summary = 'This is a review by admin'
        self.admin_review.rating = 2
        self.admin_review.ip_address = '192.168.1.3'
        self.admin_review.reviewer = admin_user
        self.admin_review.company = self.company2
        self.admin_review.save()

    def tearDown(self):
        clearUsers()
        Company.objects.all().delete()
        Review.objects.all().delete()

    def test_successful_review_create(self):
        review_count_init = Review.objects.all().count()
        factory = APIRequestFactory()
        token = getToken(ADMIN_USERNAME, USER_PASSWORD)
        user = User.objects.get(username=USER_USERNAME)
        request = factory.post('/reviews_v1/reviews',\
                json.dumps({\
                        'title': 'Review by John',
                        'summary': 'This is a review posted by John',
                        'rating': 4,
                        'ip_address': '192.168.1.1',
                        'reviewer': user.id,
                        'company': self.company1.id
                    }),\
                content_type='application/json')
        force_authenticate(request, user=user, token=token)
        view = ReviewListCreate.as_view()
        response = view(request)
        review_count_final = Review.objects.all().count()
        self.assertEqual(201, response.status_code)
        self.assertEqual(review_count_init+1, review_count_final)

    def test_bad_request_review_create(self):
        review_count_init = Review.objects.all().count()
        factory = APIRequestFactory()
        token = getToken(ADMIN_USERNAME, USER_PASSWORD)
        user = User.objects.get(username=USER_USERNAME)
        request = factory.post('/reviews_v1/reviews',\
                json.dumps({\
                        'title': 'Review by John',
                        'summary': 'This is a review posted by John',
                        'rating': 6,
                        'ip_address': '192.168.1.1',
                        'reviewer': user.id,
                        'company': self.company1.id
                    }),\
                content_type='application/json')
        force_authenticate(request, user=user, token=token)
        view = ReviewListCreate.as_view()
        response = view(request)
        review_count_final = Review.objects.all().count()
        self.assertEqual(400, response.status_code)
        self.assertEqual(review_count_init, review_count_final)

    def test_unauthorized_review_create(self):
        review_count_init = Review.objects.all().count()
        factory = APIRequestFactory()
        token = getToken(USER_USERNAME, USER_PASSWORD)
        user = User.objects.get(username=USER_USERNAME)
        admin_user = User.objects.get(username=ADMIN_USERNAME)
        request = factory.post('/reviews_v1/reviews',\
                json.dumps({\
                        'title': 'Review by wrong user',
                        'summary': 'This is a review posted by wrong user',
                        'rating': 4,
                        'ip_address': '192.168.1.1',
                        'reviewer': admin_user.id,
                        'company': self.company1.id
                    }),\
                content_type='application/json')
        force_authenticate(request, user=user, token=token)
        view = ReviewListCreate.as_view()
        response = view(request)
        review_count_final = Review.objects.all().count()
        self.assertEqual(401, response.status_code)
        self.assertEqual(review_count_init, review_count_final)

    def test_list_user_reviews(self):
        factory = APIRequestFactory()
        token = getToken(USER_USERNAME, USER_PASSWORD)
        user = User.objects.get(username=USER_USERNAME)
        request = factory.get('/reviews_v1/reviews')
        force_authenticate(request, user=user, token=token)
        view = ReviewListCreate.as_view()
        response = view(request)
        self.assertEquals(len(response.data), 1)
        self.assertEquals(response.data[0]['reviewer'], user.id)

    def test_list_admin_reviews(self):
        factory = APIRequestFactory()
        token = getToken(ADMIN_USERNAME, ADMIN_PASSWORD)
        admin_user = User.objects.get(username=ADMIN_USERNAME)
        user = User.objects.get(username=USER_USERNAME)
        request = factory.get('/reviews_v1/reviews')
        force_authenticate(request, user=admin_user, token=token)
        view = ReviewListCreate.as_view()
        response = view(request)
        self.assertGreater(len(response.data), 1)
        self.assertEquals(response.data[0]['reviewer'], user.id)
        self.assertEquals(response.data[1]['reviewer'], admin_user.id)
