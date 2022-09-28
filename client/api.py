import logging
import sys
from configparser import ConfigParser
from logging import ERROR
from typing import Any, Dict, List
from urllib.parse import quote

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError


class ProdilAPI(object):
    FILE_UPDATE_PATH = "resources/files"
    session = requests.Session()

    def __init__(
        self,
        api_url: str = None,
        email: str = None,
        password: str = None,
        config_file: str = None,
    ) -> None:
        self.API_BASE_URL = api_url
        self.AUTH_EMAIL = email
        self.AUTH_PASS = password
        self.config_file = config_file

        if config_file:
            self.load_config()

        self.check_connection()

        self.session.auth = HTTPBasicAuth(self.AUTH_EMAIL, self.AUTH_PASS)

    def load_config(self):
        parser = ConfigParser()
        parser.read(self.config_file)
        sections = ("api_base_url", "auth_email", "auth_pass")

        if not parser.has_section("prodil"):
            raise AttributeError("Bad config.")

        for section in sections:
            setattr(self, section.upper(), parser.get("prodil", section))

    def check_connection(self):
        try:
            self.session.get(self.API_BASE_URL)
        except ConnectionError:
            logging.log(ERROR, "Can not connect to API. Check your server is running.")
            sys.exit(1)

    def get(self, url: str) -> Any:
        response = self.session.get(f"{self.API_BASE_URL}/{url}")
        if response.status_code == 200:
            return response.json()
        return {}

    def get_category_id(self, category: str) -> int:
        category_id = self.get(f"categories/{quote(category)}/")
        return category_id.get("id")

    def get_categories(self) -> List[Dict[int, str]]:
        categories = self.get("categories")
        return categories

    def get_resources(
        self,
        level: str = "",
        local: str = "",
        content: str = "",
        category: str = "",
        page: int = 1,
    ) -> Dict:
        if category:
            category = self.get_category_id(category)
        if local == "__":
            local = ""

        filter_url = f"resources/?level={level}&local={local}&content={content}&category={category}&page={page}"
        return self.get(filter_url)

    def get_resource_slug(self, file_name: str) -> str:
        response = self.session.get(
            f"{self.API_BASE_URL}/resources/?file_name{file_name}"
        )
        if response.status_code == 200:
            resource = response.json()
            return resource.get("results")[0].get("slug")

    def update_resource(self, file_name: str, file_size: int, file_id: str):
        payload = {
            "file_size": file_size,
            "file_id": file_id,
        }
        self.session.put(
            url=f"{self.API_BASE_URL}/{self.FILE_UPDATE_PATH}/{file_name}/",
            json=payload,
        )

    def create_resource(self, name, file_name, file_id, file_unique_id, file_size):
        payload = {
            "name": name,
            "file_name": file_name,
            "file_id": file_id,
            "file_unique_id": file_unique_id,
            "file_size": file_size,
        }
        return self.session.post(url=f"{self.API_BASE_URL}/resources/", json=payload)
