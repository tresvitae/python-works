import requests
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
repo_name = "my-peex-test-repo7"

response = client.create_repository(repo_name)

if response:
    print('Repository created successfully!')
else:
    print('Failed to create repository.')

#Get latest sha and create new branch
original_branch_name = "main"
new_branch_name = "developer"
owner_name = "tresvitae"

sha_id = client.get_branch_sha(owner_name, repo_name, original_branch_name)
response = client.create_branch(owner_name, repo_name, new_branch_name, sha_id)
print(sha_id)
if response:
    print(f'New branch {new_branch_name} created successfully from {sha_id}.')
else:
    print('Failed to create the branch.')


#Put the tag on the initial commit of the new branch
tag_name = "v1.0.0"
response = client.create_tag(owner_name, repo_name, sha_id, tag_name)

print(sha_id)
if response:
    print(f'Tag {tag_name} added successfully!')
else:
    print(f'Failed to add tag to initial commit in {new_branch_name} branch.')



'''
echo f'# {repo_name}' >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/tresvitae/my-peex-test-repo7.git
git push -u origin main
'''