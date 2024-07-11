# data_manager.py
import json
from your_app import db
from your_app.models import User

class DataManager:
    def create_user(self, user_data: dict):
        raise NotImplementedError

    def update_user(self, user_id: int, data: dict):
        raise NotImplementedError

class FileDataManager(DataManager):
    def __init__(self, filepath='users.json'):
        self.filepath = filepath

    def _read_file(self):
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _write_file(self, data):
        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=4)

    def create_user(self, user_data: dict):
        users = self._read_file()
        users.append(user_data)
        self._write_file(users)
        return user_data

    def update_user(self, user_id: int, data: dict):
        users = self._read_file()
        for user in users:
            if user['id'] == user_id:
                user.update(data)
                break
        self._write_file(users)
        return data

class DBDataManager(DataManager):
    def create_user(self, user_data: dict):
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def update_user(self, user_id: int, data: dict):
        user = User.query.get(user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

