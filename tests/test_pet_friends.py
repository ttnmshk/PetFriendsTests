from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os

pf = PetFriends()

#1
def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    return status, result
#2
def test_add_new_pet_without_photo(name='Kot', animal_type='cat', age='10'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'добавлен {result}')
#3
def test_add_photo_of_existing_pet(pet_id='65330359-b926-4f6a-b6d7-85a4a29ed2a7',
                                   pet_photo=r'C:\Users\ttnms\PycharmProjects\PetFriendsTesting\images\fatty.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_photo_of_existing_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] != pet_photo
    print(f'\n фото добавлено {result}')
#4
def test_get_api_key_invalid_pass(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    return status, result
#5
def test_get_api_key_invalid_email(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    return status, result
#6
def test_get_api_key_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    return status, result
#7
def test_add_pet_with_valid_data_empty_field():
    name = ''
    animal_type = ''
    age = ''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
#8
def test_successful_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 200
    assert pet_id not in my_pets.values()
#9
def test_get_all_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
