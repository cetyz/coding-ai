import requests
from typing import Dict, Any
import mimetypes

def fetch_github_repo(repo_url: str) -> Dict[str, Any]:
    """
    Fetches all files from a given GitHub repository URL and returns their content.
    """
    # Extract owner and repo from the URL
    parts = repo_url.split('/')
    owner, repo = parts[-2], parts[-1]

    # GitHub API URL to get the repo content
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/"

    def get_contents(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_files(contents, path=""):
        files = {}
        for item in contents:
            item_path = f"{path}/{item['name']}" if path else item['name']
            if item['type'] == 'file':
                mime_type, _ = mimetypes.guess_type(item['download_url'])
                if mime_type and (mime_type.startswith('image/') or mime_type.startswith('audio/') or mime_type.startswith('video/')):
                    files[item_path] = 'Binary file'
                else:
                    file_content = requests.get(item['download_url']).text
                    files[item_path] = file_content
            elif item['type'] == 'dir':
                dir_contents = get_contents(item['url'])
                files.update(fetch_files(dir_contents, item_path))
        return files

    contents = get_contents(api_url)
    repo_files = fetch_files(contents)

    if '.gitattributes' in repo_files.keys():
        repo_files.pop('.gitattributes')
    if '.gitignore' in repo_files.keys():
        repo_files.pop('.gitignore')

    

    # Returning the collected data in JSON STRING format
    return str(repo_files)


tool_dict = {
    'fetch_github_repo': fetch_github_repo
}

if __name__ == '__main__':
    url = 'https://github.com/cetyz/coding-ai'
    response = fetch_github_repo(url)
    print(response)