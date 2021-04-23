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
    pr_detail = [requests.get(item["pull_request"]["url"], headers=headers).json() for item in pull_requests["items"]]
    result_search = {}

    for pr in pr_detail:
        if pr["base"]["repo"]["name"] not in result_search:
            result_search[pr["base"]["repo"]["name"]] = {
                "url": pr["base"]["repo"]["html_url"],
                "star": pr["base"]["repo"]["stargazers_count"],
                "pr_unmerged": [],
                "pr_merged": []
            }
        if pr["merged_at"] is None:
            result_search[pr["base"]["repo"]["name"]]["pr_unmerged"].append(
                {pr["html_url"]: {"comments": pr["comments"], "number": pr["number"]}})
        else:
            result_search[pr["base"]["repo"]["name"]]["pr_merged"].append(
                {pr["html_url"]: {"comments": pr["comments"], "number": pr["number"]}})

    return result_search
