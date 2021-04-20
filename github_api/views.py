import requests
from django.shortcuts import render


def view_search(request):
    args = {}
    if request.GET.get('search', ''):
        owner = request.GET.get('search', '')
        token = "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"
        url = "https://api.github.com/search/issues"
        headers = {"Authorization": f"token {token}"}
        params = {"q": f"author:{owner} type:pr"}
        r = requests.get(url, headers=headers, params=params)
        try:
            r.raise_for_status()
        except Exception:
            args["user_not_found"] = True
            return render(request, template_name='search.html', context={"args": args})

        pr = r.json()
        pr_detail = [requests.get(item["pull_request"]["url"], headers=headers).json() for item in pr["items"]]
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
                result_search[pr["base"]["repo"]["name"]]["pr_unmerged"].append({pr["html_url"]: {"comments": pr["comments"], "number": pr["number"]}})
            else:
                result_search[pr["base"]["repo"]["name"]]["pr_merged"].append({pr["html_url"]: {"comments": pr["comments"], "number": pr["number"]}})

        if not result_search:
            args["message"] = True

        return render(request, template_name='search.html', context={"result_search": result_search, "args": args})

    return render(request, template_name='search.html')
