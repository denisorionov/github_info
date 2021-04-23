import requests

token = "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"


def search(token, owner):
    url = "https://api.github.com/search/issues"
    headers = {"Authorization": f"token {token}"}
    params = {"q": f"author:{owner} type:pr"}
    response = requests.get(url, headers=headers, params=params)

    try:
        response.raise_for_status()
    except Exception:
        return None

    pull_requests = response.json()
    pull_request_detail = [requests.get(item["pull_request"]["url"], headers=headers).json() for item in pull_requests["items"]]
    result_search = {}

    for pull_request in pull_request_detail:
        if pull_request["base"]["repo"]["name"] not in result_search:
            result_search[pull_request["base"]["repo"]["name"]] = {
                "url": pull_request["base"]["repo"]["html_url"],
                "star": pull_request["base"]["repo"]["stargazers_count"],
                "pr_unmerged": [],
                "pr_merged": []
            }
        if pull_request["merged_at"] is None:
            result_search[pull_request["base"]["repo"]["name"]]["pr_unmerged"].append(
                {pull_request["html_url"]: {"comments": pull_request["comments"], "number": pull_request["number"]}})
        else:
            result_search[pull_request["base"]["repo"]["name"]]["pr_merged"].append(
                {pull_request["html_url"]: {"comments": pull_request["comments"], "number": pull_request["number"]}})

    return result_search
