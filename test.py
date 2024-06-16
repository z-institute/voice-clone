import requests


class UserAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user_points(self):
        url = f"{self.base_url}/api/users/points"
        headers = {
            "accept": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code, response.text)
            return None

    def get_user_profile(self, user_id):
        url = f"{self.base_url}/api/users/{user_id}/profile"
        headers = {
            "accept": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code, response.text)
            return None

    def get_user_point(self, user_id):
        url = f"{self.base_url}/api/users/{user_id}/point"
        headers = {
            "accept": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code, response.text)
            return None

    def update_user_point(self, user_id, point_type, point_value):
        url = f"{self.base_url}/api/users/{user_id}/point"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        data = {"type": point_type, "point": point_value}

        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code, response.text)
            return None

    def get_user_referral(self, user_id):
        url = f"{self.base_url}/api/users/{user_id}/referral"
        headers = {
            "accept": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code, response.text)
            return None

    def create_user_referral(self, user_id, referral_user_id):
        url = f"{self.base_url}/api/users/{user_id}/referral"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        data = {"referral_user_id": referral_user_id}

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code, response.text)
            return None

    def delete_user_referral(self, user_id):
        url = f"{self.base_url}/api/users/{user_id}/referral"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(response)
            return None


# 使用範例
base_url = "http://34.72.204.98:8080"
api = UserAPI(base_url)

# test_user_id = "771281904" # james yeh
test_user_id = "915540009" # tina
test_user_referrer = "1199691622"

test_cases = [
    (f"get {test_user_id} points", lambda: api.get_user_point(test_user_id)),
    (
        f"add {test_user_id} 1000 points",
        lambda: api.update_user_point(test_user_id, "for_test", 10000),
    ),
    (
        f"get {test_user_id} points again",
        lambda: api.get_user_point(test_user_id),
    ),
    # (
    #     f"sub {test_user_id} 10 points",
    #     lambda: api.get_user_profile(test_user_id),
    # ),
    # (
    #     f"get {test_user_id} referrer",
    #     lambda: api.get_user_referral(test_user_id),
    # ),
    # (
    #     f"add {test_user_id} referrer from {test_user_referrer}",
    #     lambda: api.create_user_referral(test_user_id, test_user_referrer),
    # ),
    # (
    #     f"get {test_user_id} referrer again",
    #     lambda: api.get_user_referral(test_user_id),
    # ),
    # (
    #     f"delete {test_user_id} referrer",
    #     lambda: api.delete_user_referral(test_user_id),
    # ),
    # (
    #     f"get {test_user_id} referrer again",
    #     lambda: api.get_user_referral(test_user_id),
    # ),
    # (
    #     f"sub {test_user_id} 300 points",
    #     lambda: api.update_user_point(test_user_id, "for_test", -300),
    # ),
    # (
    #     f"sub {test_user_id} 50 points",
    #     lambda: api.update_user_point(test_user_referrer, "for_test", -50),
    # ),
    # ("get all user cases", lambda: api.get_user_points()),
]

for case, func in test_cases:
    print("======", case, "======")
    print(func())
