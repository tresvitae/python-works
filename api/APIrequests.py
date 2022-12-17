import requests
from os import environ
import base64

api_token = environ['GITHUB_API_TOKEN']

class GitHubClient:
    #Initialize the client with the api token
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = 'https://api.github.com/'
        self.headers = {
            'Authorization': f'token {api_token}',
            'Content-Type': 'application/json'
        }

    def create_repository(self, name: str):
        """
        Create a new public repository on GitHub.
        """
        url = f'{self.base_url}user/repos'
        data = {
            'name': name,
            'private': False
            #"has_issues": True,
            #"has_projects": True,
            #"has_wiki": True
        }

        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def create_initial_commit(self, owner: str, repo: str, branch: str, message: str, content: str):
        """
        Create initial commit on the new repository.
        """
        url = f'{self.base_url}repos/{owner}/{repo}/contents/README.md'
        data = {
            'message': message,
            'content': content#,
            #'branch': branch
        }

        try:
            response = requests.put(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        
    def get_branch_sha(self, owner: str, repo: str, branch: str):
        """
        Get the SHA of the latest commit on the specified branch.
        """
        url = f'{self.base_url}repos/{owner}/{repo}/branches/{branch}'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()['commit']['sha']
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def create_branch(self, owner: str, repo: str, branch: str, sha: str='main'):
        """
        Create a new branch on a repository.
        """
        url = f'{self.base_url}repos/{owner}/{repo}/git/refs'
        data = {
            'ref': f'refs/heads/{branch}',
            'sha': sha
        }

        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def create_tag(self, owner: str, repo: str, sha: str, tag: str):
        """
        Create a new tag on an initial commit of the specified branch.
        """
        url = f'{self.base_url}repos/{owner}/{repo}/git/tags'
        data = {
            'tag': tag,
            'message': f'Tagging initial commit of branch {tag}',
            'object': sha,
            'type': 'commit'
        }

        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

#Create instnace of the GitHubClient class
client = GitHubClient(api_token)

#Create the repository 
repo_name = "my-peex-test-repo5"

response = client.create_repository(repo_name)

if response:
    print('Repository created successfully!')
else:
    print('Failed to create repository.')

# Create the initial commit in the new repository
owner_name = "tresvitae"
original_branch_name = "master"
message = 'Initial commit'

#Encode to Base64 fromat
encode_test = base64.b64encode(b'PEEX I WANNA GET PROMOTION')
content = encode_test.decode()

response = client.create_initial_commit(owner_name, repo_name, original_branch_name, message, content)

if response:
    print(f'New commit with message {base64.b64decode(content)} created successfully!.')
else:
    print('Failed to create initial commit.')

#Get latest sha and create new branch
new_branch_name = "developer"

sha_id = client.get_branch_sha(owner_name, repo_name, original_branch_name)
response = client.create_branch(owner_name, repo_name, new_branch_name, sha_id)

if response:
    print(f'New branch {new_branch_name} created successfully from {sha_id}.')
else:
    print('Failed to create the branch.')

#Put the tag on the initial commit of the new branch
tag_name = "v1.0.0"

response = client.create_tag(owner_name, repo_name, sha_id, tag_name)

if response:
    print(f'Tag {tag_name} added successfully!')
else:
    print(f'Failed to add tag to initial commit in {new_branch_name} branch.')

