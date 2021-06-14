# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

def create_issue(project="NOSVG", summary=None, description=None, issue_type=None, fix_version=None, assignee_name=None):
  url = "https://jira.dzsi.com/rest/api/2/issue"
  username = "ha.nguyen"
  password = ""
  auth = HTTPBasicAuth(username, password)
  headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
  }
  fields = {}
  issue_dict = {}
  issue_dict["project"] = {'key': project}
  issue_dict['summary'] = summary
  issue_dict['description'] = description
  issue_dict['issuetype'] = {'name': issue_type}
  issue_dict["fixVersions"] = [{"name": fix_version}]
  issue_dict['assignee'] = {'name': assignee_name} 
  fields["fields"] = issue_dict
  payload = json.dumps(fields)# convert object python to json string
  print(type(payload))
  response = requests.request(
     "POST",
     url,
     data=payload,
     headers=headers,
     auth=auth
  )

  print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
  return  

if __name__ == '__main__':
  create_issue(summary='Handt_testing', fix_version='Handt_python', description="Ha test", issue_type="Bug", assignee_name="ha.nguyen")
#Milestone
#customfield_10842

