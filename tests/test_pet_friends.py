from api import PetFriends
from setings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pets_with_valid_data(name='Кот', animal_type='кот', age='3', pet_photo='images/cat.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.normpath(pet_photo)
    #pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Кот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Василий', animal_type='кот', age=5):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


# Добавленные тесты

def test_simple_add_new_pet_with_valid_data(name='Дог', animal_type='собака', age='4'):
    """Проверяем возможность добавления питомца без фотографии"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_no_foto(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo(pet_photo='images/dog.jpeg'):
    """Проверяем возможность добавления фотографии питомца."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] != ''


def test_add_new_pet(name='//////', animal_type='******', age='Four', pet_photo='images/cat5.jpg'):
    """Проверяем добавления питомца с не корректными данными и несуществующим фото"""

    pet_photo = os.path.normpath(pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name

def test_get_api_key_for_incorrect_user(email='allert@com', password='123'):
    """ Проверяем что запрос api ключа возвращает статус 403 при введении некорректных данных"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_add_new_pets_with_incorrect_photo(name='Василий', animal_type='кот',
                                           age='3', pet_photo='images/cat2.gif'):
    """Проверка добавления питомца с типом фотографии gif.
    Баг - питомец добавляется, фото у добавленного питомца не отображается"""

    pet_photo = os.path.normpath(pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] == name


def test_add_new_pets_with_incorrect_name(name=None, animal_type='кот', age='3',
                                          pet_photo='images/cat1.jpg'):
    """Проверяем что при попытке добавить питомца с некорректным именем возвращается статус 400"""

    pet_photo = os.path.normpath(pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pets_with_incorrect_animal_type(name='Борис', animal_type=None, age='3',
                                                 pet_photo='images/cat1.jpg'):
    """Проверяем что при попытке добавить питомца с некорректным типом возвращается статус 400"""

    pet_photo = os.path.normpath(pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pets_with_incorrect_age(name='Болт', animal_type='кот', age=None,
                                         pet_photo='images/cat1.jpg'):
    """Проверяем что при попытке добавить питомца с некорректным возрастом возвращает статус 400"""

    pet_photo = os.path.normpath(pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_update_pets_with_incorrect_age(name='Март', animal_type='кот', age=-5):
    """Проверяем что произойдет при обновлении информации с указанием
    отрицательного возраста животного"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status != 200
    else:
        raise Exception("There is no my pets")


def test_add_new_pets_with_incorrect_auth_key(name='Барсук', anymal_type='кот',
                                              age='3', pet_photo='images/cat.jpeg'):
    """Проверяем что произойдет при попытке добавить питомца используя некорректный auth_key"""

    pet_photo = os.path.normpath(pet_photo)
    auth_key = '123'
    status, result = pf.add_new_pet_with_incorrect_auth_key(auth_key, name, anymal_type, age, pet_photo)
    assert status == 403

