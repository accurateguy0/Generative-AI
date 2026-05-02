import os
from llama_index.readers.github import GithubRepositoryReader, GithubClient

def ingest_pull_request_files(owner, repo, pr_number):
    
    github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
    
    loader = GithubRepositoryReader(
        github_client=github_client,
        owner=owner,
        repo=repo,
        use_parser=True,
        verbose=True,
        filter_file_extensions=[".py", ".js", ".sql"],
    )
    
    
    documents = loader.load_data(branch="main")
    return documents
