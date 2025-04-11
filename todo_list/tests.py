import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from todo_list.models import ToDoList

TODO_LIST_URL = '/api/custom-todos/'
REGISTER_URL = '/api/register/'
LOGIN_URL = '/api/login/'

# Setup Fixtures
@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password='password123')

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client

@pytest.fixture
def create_todo_list():
    todos = [
        ToDoList.objects.create(title='Buy milk', description='Skim milk'),
        ToDoList.objects.create(title='Buy eggs', description='Dozen eggs'),
        ToDoList.objects.create(title='Clean the bathroom', description='Thoroughly'),
        ToDoList.objects.create(title='Finish homework', description='Due at 10:00 PM tonight'),
    ]
    print([todo.id for todo in todos])  # Debug print to check the IDs
    return todos

# ------ Test ToDo List --------

# Get List
@pytest.mark.django_db
class TestGetToDoList:
    def test_get_list(self, authenticated_client, create_todo_list):
        response = authenticated_client.get(TODO_LIST_URL)
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) == len(create_todo_list)

    def test_get_list_unauthorized(self, api_client):
        response = api_client.get(TODO_LIST_URL)
        assert response.status_code == 401

    def test_get_list_bad_token(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION='Token Invalid')
        response = api_client.get(TODO_LIST_URL)
        assert response.status_code == 401

    def test_get_empty_list(self, authenticated_client):
        response = authenticated_client.get(TODO_LIST_URL)
        assert response.status_code == 200
        assert response.data == []

# Test add request
@pytest.mark.django_db
class TestCreateTodo:
    @pytest.fixture
    def json(self):
        return {'title': 'Buy milk', 'description': 'buy skim milk'}
    
    def test_create_todo(self, authenticated_client, json):
        response = authenticated_client.post(TODO_LIST_URL, json, format='json')
        assert response.status_code == 201
        assert response.data['title'] == json['title']
        assert response.data['description'] == json['description']

    def test_create_todo_unauthorized(self, api_client, json):
        response = api_client.post(TODO_LIST_URL, json, format='json')
        assert response.status_code == 401

    def test_create_todo_bad_token(self, api_client, json):
        api_client.credentials(HTTP_AUTHORIZATION='Token Invalid')
        response = api_client.post(TODO_LIST_URL, json, format='json')
        assert response.status_code == 401

    def test_create_todo_missing_title(self, authenticated_client):
        json = {'description': 'buy skim milk'}
        response = authenticated_client.post(TODO_LIST_URL, json, format='json')
        assert response.status_code == 400
        assert 'title' in response.data
        
    def test_create_todo_empty_title(self, authenticated_client):
        json = {'title': '', 'description': 'buy skim milk'}
        response = authenticated_client.post(TODO_LIST_URL, json, format='json')
        assert response.status_code == 400
        assert 'title' in response.data
        
    def test_create_todo_missing_description(self, authenticated_client):
        json = {'title': 'Buy milk'}
        response = authenticated_client.post(TODO_LIST_URL, json, format='json')
        assert response.status_code == 201
        assert response.data['title'] == json['title']
        
    def test_create_todo_extra_field(self, authenticated_client):
        json = {'title': 'Buy milk', 'description': 'buy skim milk', 'huh':'test' }
        response = authenticated_client.post(TODO_LIST_URL, json, format='json')
        assert response.status_code == 201
        assert 'huh' not in response.data
        
    def test_item_added(self, authenticated_client, create_todo_list, json):
        post_response = authenticated_client.post(TODO_LIST_URL, json, format='json')
        assert post_response.status_code == 201
        get_reponse = authenticated_client.get(TODO_LIST_URL)
        assert len(get_reponse.data) == len(create_todo_list)+1
    
# Test Get Item
@pytest.mark.django_db
class TestGetToDoItem:
    def test_get_todo_item(self, authenticated_client, create_todo_list):
        response = authenticated_client.get(TODO_LIST_URL + '1')
        assert response.status_code == 200
        assert response.data['title'] == create_todo_list[0].title
    
    def test_get_no_item(self, authenticated_client, create_todo_list):
        response = authenticated_client.get(TODO_LIST_URL + '100')
        assert response.status_code == 404
        
    def test_get_empty_list(self, authenticated_client):
        response = authenticated_client.get(TODO_LIST_URL + '100')
        assert response.status_code == 404

    def test_get_todo_item_unauthorized(self, api_client, create_todo_list):
        response = api_client.get(TODO_LIST_URL + '1')
        assert response.status_code == 401

    def test_create_todo_item_bad_token(self, api_client, create_todo_list):
        api_client.credentials(HTTP_AUTHORIZATION='Token Invalid')
        response = api_client.get(TODO_LIST_URL + '1')
        assert response.status_code == 401
        
    def test_get_bad_key(self, authenticated_client, create_todo_list):
        response = authenticated_client.get(TODO_LIST_URL + 'help')
        assert response.status_code == 404

# Test Update ToDo List
@pytest.mark.django_db
class TestUpdateToDo:
    @pytest.fixture
    def json(self):
        return {'title': 'Updated Title', 'description': 'Updated Description'}
            
    def test_update_todo(self, authenticated_client, create_todo_list, json):
        response = authenticated_client.put(TODO_LIST_URL + '1', json, format='json')
        assert response.status_code == 200
        assert response.data['title'] == json['title']
        assert response.data['description'] == json['description']
    
    def test_update_no_element(self, authenticated_client, create_todo_list, json):
        response = authenticated_client.put(TODO_LIST_URL + '100', json, format='json')
        assert response.status_code == 404
    
    def test_update_unauthorized(self, api_client, create_todo_list, json):
        response = api_client.put(TODO_LIST_URL + '1', json, format='json')
        assert response.status_code == 401
        
    def test_update_bad_token(self, api_client, create_todo_list, json):
        api_client.credentials(HTTP_AUTHORIZATION='Token Invalid')
        response = api_client.put(TODO_LIST_URL + '1', json, format='json')
        assert response.status_code == 401 

    def test_update_missing_title(self, authenticated_client, create_todo_list):
        json = { 'description': 'buy skim milk'}
        response = authenticated_client.put(TODO_LIST_URL + '2', json, format='json')
        assert response.status_code == 400
        assert 'title' in response.data
     
    def test_update_empty_title(self, authenticated_client, create_todo_list):
        json = {'title': '', 'description': 'buy skim milk'}
        response = authenticated_client.put(TODO_LIST_URL + '2', json, format='json')
        assert response.status_code == 400
        assert 'title' in response.data
        
    def test_update_missing_description(self, authenticated_client, create_todo_list):
        json = {'title': 'Buy milk'}
        response = authenticated_client.put(TODO_LIST_URL + '2', json, format='json')
        assert response.status_code == 200
        assert response.data['title'] == json['title']
        
    def test_update_extra_field(self, authenticated_client, create_todo_list):
        json = {'title': 'Buy milk', 'description': 'buy skim milk', 'huh':'test' }
        response = authenticated_client.put(TODO_LIST_URL + '2', json, format='json')
        assert response.status_code == 200
        assert 'huh' not in response.data

# Test Delete Item
@pytest.mark.django_db
class TestDeleteToDo:
    def test_delete(self, authenticated_client, create_todo_list):
        response = authenticated_client.delete(TODO_LIST_URL + '2')
        assert response.status_code == 204
        
    def test_delete_unauthorized(self, api_client, create_todo_list):
        response = api_client.delete(TODO_LIST_URL + '2')
        assert response.status_code == 401
        
    def test_delete_bad_token(self, api_client, create_todo_list):
        api_client.credentials(HTTP_AUTHORIZATION='Token Invalid')
        response = api_client.delete(TODO_LIST_URL + '1')
        assert response.status_code == 401
        
    def test_delete_unknown(self, authenticated_client, create_todo_list):
        response = authenticated_client.delete(TODO_LIST_URL + str(len(create_todo_list) + 1))
        assert response.status_code == 404
        
    def test_list_after_delete(self, authenticated_client, create_todo_list):
        deleteresponse = authenticated_client.delete(TODO_LIST_URL + '2')
        assert deleteresponse.status_code == 204
        getresponse = authenticated_client.get(TODO_LIST_URL)
        assert len(getresponse.data) == len(create_todo_list)-1
        getitemresponse = authenticated_client.get(TODO_LIST_URL + '2')
        assert getitemresponse.status_code == 404

# Test Register
@pytest.mark.django_db
class TestRegister:
    def test_register(self, api_client):
        newuser = { "username": "newuser", "password":"password123!"}
        response = api_client.post(REGISTER_URL, newuser, format='json')
        assert response.status_code == 201
        assert response.data['username'] == newuser['username']
    
    def test_duplicate_register(self, api_client):
        newuser = {"username": "newuser", "password":"password123!"}
        response = api_client.post(REGISTER_URL, newuser, format='json')
        assert response.status_code == 201
        dupe_response = api_client.post(REGISTER_URL, newuser, format='json')
        assert dupe_response.status_code == 400
    
    def test_no_username(self, api_client):
        newuser = { "password":"password123!"}
        response = api_client.post(REGISTER_URL, newuser, format='json')
        assert response.status_code == 400
    
    def test_no_password(self, api_client):
        newuser = { "username":"test!"}
        response = api_client.post(REGISTER_URL, newuser, format='json')
        assert response.status_code == 400

@pytest.mark.django_db
class TestLogin:
    def test_login(self, api_client, test_user):
        login = { "username":"testuser", "password":"password123"}
        response = api_client.post(LOGIN_URL, login, format='json')
        assert response.status_code == 200
        assert 'token' in response.data
        
    def test_login_wrong_username(self, api_client, test_user):
        login = { "username":"badusername", "password":"password123"}
        response = api_client.post(LOGIN_URL, login, format='json')
        assert response.status_code == 400
        assert response.data['error'] == "Invalid credentials"

    def test_login_wrong_username(self, api_client, test_user):
        login = { "username":"testuser", "password":"badpassword123"}
        response = api_client.post(LOGIN_URL, login, format='json')
        assert response.status_code == 400
        assert response.data['error'] == "Invalid credentials"
        
    def test_no_user(self, api_client):
        login = { "username":"testuser", "password":"password123"}
        response = api_client.post(LOGIN_URL, login, format='json')
        assert response.status_code == 400
        assert response.data['error'] == "Invalid credentials"
        
    def test_missing_username(self, api_client):
        login = { "password":"password123" }
        response = api_client.post(LOGIN_URL, login, format='json')
        assert response.status_code == 400
        assert response.data['error'] == "Invalid credentials"
        
    def test_missing_password(self, api_client):
        login = { "username":"testuser" }
        response = api_client.post(LOGIN_URL, login, format='json')
        assert response.status_code == 400
        assert response.data['error'] == "Invalid credentials"