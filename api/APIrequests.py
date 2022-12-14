import requests
import base64
from os import environ

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

    def create_branch(self, owner: str, repo: str, branch_name: str, sha: str=None):
        """
        Create a new branch on a repository.
        """
        url = f'{self.base_url}repos/{owner}/{repo}/git/refs'
        data = {
            'ref': f'refs/heads/{branch_name}',
            'sha': sha
        }

        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def create_tag(self, repo: str, sha: str, tag: str):
        """
        Create a new tag on an initial commit of the specified branch.
        """
        url = f'{self.base_url}repos/{repo}/git/tags'
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
repo_name = "my-peex-test-repo"
response = client.create_repository(repo_name)

if response:
    print('Repository created successfully!')
else:
    print('Failed to create repository')

#Create new branch
branch_name = "test-branch"
response = client.create_branch(repo_name, branch_name)

#Put the tag on the initial commit of the new branch
commit_sha = response['commit']['sha']
tag_name = "my-new-tag"
response = client.put_tag(repo_name, commit_sha, tag_name)