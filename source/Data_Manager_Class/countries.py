# country_data_manager.py
import json
from your_app import db
from your_app.models import Country

class CountryDataManager:
    def get_all_countries(self) -> list:
        raise NotImplementedError

    def get_country(self, code: str) -> Country:
        raise NotImplementedError

    def create_country(self, name: str, code: str) -> Country:
        raise NotImplementedError

class FileCountryDataManager(CountryDataManager):
    def __init__(self, filepath='countries.json'):
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

    def get_all_countries(self) -> list:
        return self._read_file()

    def get_country(self, code: str) -> Country:
        countries = self._read_file()
        for country in countries:
            if country['code'] == code:
                return Country(**country)
        return None

    def create_country(self, name: str, code: str) -> Country:
        countries = self._read_file()
        new_country = {'name': name, 'code': code}
        countries.append(new_country)
        self._write_file(countries)
        return Country(**new_country)

class DBCountryDataManager(CountryDataManager):
    def get_all_countries(self) -> list:
        return Country.query.all()

    def get_country(self, code: str) -> Country:
        return Country.query.get(code)

    def create_country(self, name: str, code: str) -> Country:
        new_country = Country(name=name, code=code)
        db.session.add(new_country)
        db.session.commit()
        return new_country

