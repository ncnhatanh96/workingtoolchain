from datetime import datetime
import json
from jira import JIRA
import dzsi

class WrapJira(JIRA):

    def __init__(self, url, username, password):
        JIRA.__init__(self, server=url, basic_auth=(username, password))
        self.__username = username
        self.__password = password

    def search_issue_by_username(self, username):
        return

    def search_issue_by_milestone(self, milestone):
        return

    def set_issue_status(self, issue=None, new_status=None):
        return

    def get_issue_status(self, issue=None):
        return

    def set_issue_assignee(self, issue=None, new_assignee=None):
        return

    def get_issue_assignee(self, issue=None):
        return

    def set_issue_remainingestimate(self, issue=None, new_remainingestimate=None):
        return

    def get_issue_remainingestimate(self, issue=None):
        return

    def set_issue_customfield(self, issue=None, custom_field=None, new_customefield_value=None):
        return

    def set_milestone_attribute(self, milestone_id=None, attr_name=None, new_attrvalue=None):
        return

    def get_milestone_attribute(self, milestone_id=None, attr_name=None):
        return

    def create_issue(self, issue_dict=None):
        return

    def delete_issue(self, issue=None):
        return

    def clone_issue(self, issue=None):
        return

    def add_worklog(self, issue=None, time_spent=None, adjust_estimate=True,
                    new_estimate=None, reduce_by=None, started=None, project_id=None,
                    site=None, domain_id=None, night_overtime=False, wbs=None):
        data = {}

        data['user'] = self.__username

        if issue is not None:
            data['issueKey'] = issue

        if adjust_estimate is not None:
            data['autoAdjustRemaining'] = adjust_estimate

        if night_overtime is not None:
            data['nightOvertime'] = night_overtime

        data['process'] = {
            "id": dzsi.PAIR_WBS_ID_TITLE.get(wbs),
            "technicalDomain": True,
            "haschildren": False,
            "title": wbs,
            "type":''
        }

        data['projectSites'] = [{
            "project": 'PJT:2062',
            "site":'CHT'
        }]

        now = datetime.now()
        data['started'] = now.strftime("%Y-%m-%dT 9:00")

        data['technologyDomain'] = {
            "id":"3",
            "name":"GPON"
        }

        if time_spent is not None:
            data['timeSpent'] = time_spent
            data['timeSpentSecond'] = int(time_spent)*3600

        print(json.dumps(data, indent=4))
        url = dzsi.LOGWORK_URL
        r = self._session.post(url, data=json.dumps(data)) #pylint
        return
