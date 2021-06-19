from datetime import datetime
import json
from jira import JIRA
import dzsi


class WrapJira(JIRA):

    def __init__(self, url, username, password, team=None):
        JIRA.__init__(self, server=url, basic_auth=(username, password))
        self.__username = username
        self.__password = password
        self.__team     = team
        self.__user_issuelist      = {}
        self.__milestone_issuelist = {}
        self.__milestone_list      = {}
        self.__Dzsi = dzsi.Dzsi()

        #Update milestone list following TEAM
        r = self._session.get(dzsi.MILESTONE_BIZGW_URL)
        if team == 'BIZGW':
            r = self._session.get(dzsi.MILESTONE_BIZGW_URL)
        elif team == 'NETWORK':
            r = self._session.get(dzsi.MILESTONE_NETWORK_URL)
        elif team == 'PLATFORM':
            r = self._session.get(dzsi.MILESTONE_PLATFORM_URL)
        elif team is None:
            return

        for milestone in r.json()["results"]:
            self.__milestone_list[milestone["id"]] = milestone["name"]

    def search_issue_by_username(self, username, maxResults=5):

        for issue in self.search_issues('project=NOSVG and assignee={}'.format(username), maxResults=maxResults):
            print('{}: {}'.format(issue.key, issue.fields.summary))
            self.__user_issuelist[issue.key] = issue.fields.summary

        return

    def search_issue_by_milestone(self, milestone):

        for issue in self.search_issues('project=NOSVG and milestone={}'.format(milestone)):
            print('{}: {}'.format(issue.key, issue.fields.summary))

        return

    def set_issue_status(self, issuekey=None, new_status=None):
        issue = self.issue(issuekey)
        if new_status == str(issue.fields.status):
            return
        for transition in self.__Dzsi.get_transitionId_flow cur_status=str(issue.fields.status),\
                                    new_status=new_status)[1::]:
            self.transition_issue(issue, transition)
        return

    def get_issue_status(self, issuekey=None):
        issue = self.issue(issuekey)
        return issue.fields.status

    def set_issue_assignee(self, issuekey=None, new_assignee=None):
        issue = self.issue(issuekey)
        self.assign_issue(issue, new_assignee)
        return

    def get_issue_assignee(self, issuekey=None):
        issue = self.issue(issuekey)
        return issue.fields.assignee

    def set_issue_remainingestimate(self, issuekey=None, new_remainingestimate=None):
        issue = self.issue(issuekey)
        if new_remainingestimate is None:
            return
        issue.update(fields={'timetracking': {'remainingEstimate': new_remainingestimate}})
        return

    def get_issue_remainingestimate(self, issuekey=None):
        issue = self.issue(issuekey)
        return issue.fields.timetracking.remainingEstimate

    def set_issue_customfield(self, issuekey=None, custom_field=None,\
                                new_customefield_value=None):
        return

    def set_milestone_attribute(self, issuekey=None, milestone_id=None, \
                                    attr_name=None, new_attrvalue=None):
        return

    def get_milestone_attribute(self, milestone_id=None, attr_name=None):
        return

    def create_issue(self, project='NOSVG', issuetype='Bug', summary=None, description=None,
                     priority='Major', assignee=None, components=None, fixVersions=None,
                     outwardIssue=None, type='Blocks'):
        issue_dict = {}

        issue_dict['project'] = {'key': project}
        issue_dict['issuetype'] = {'name': issuetype}

        if summary is None:
            return
        else:
            issue_dict['summary'] = summary

        if description is not None:
            issue_dict['description'] = description
        else:
            issue_dict['description'] = 'h1.Symptom/Requirement\\\\ \nh1.Rootcause\\\\\
                                            \nh1.Solution\\\\ \nh1.Selftest'

        issue_dict['priority'] = {"name": priority}

        if assignee is None:
            issue_dict['assignee'] = {
                "name": self.__username
            }
        else:
            issue_dict['assignee'] = {
                "name": assignee
            }

        issue_dict['components'] = [
            {'name': components}
        ]

        if fixVersions is None:
            return
        else:
            issue_dict['fixVersions'] = [
                {'name': fixVersions}
            ]
        issue_dict["customfield_10842"] = 1834
        issue = self.create_issue(self, fields=issue_dict)
        if outwardIssue is not None:
            self.create_issue_link(self, type=type, inwardIssue=issue.key,\
                                    outwardIssue=outwardIssue, comment=None)
        return

    def delete_issue(self, issue=None):
        return

    def clone_issue(self, issuekey=None, auto_link_issue=True, fixVersions=None,
                    components=None):

        if issuekey is not None:
            issue = self.issue(issuekey)
        else:
            return

        if auto_link_issue == True:
            clone_issue = self.create_issue(summary=issue.fields.summary,\
                                            description=issue.fields.description,\
                                            outwardIssue=issue.key, components=components,
                                            fixVersions=fixVersions)
        else:
            clone_issue = self.create_issue(summary=issue.fields.summary,\
                                            description=issue.fields.description,\
                                            components=components, fixVersions=fixVersions)
        return

    def add_worklog(self, issuekey=None, time_spent=None, adjust_estimate=True,
                    new_estimate=None, reduce_by=None, started=None, project_id=None,
                    site=None, domain_id=None, night_overtime=False, wbs=None):
        data = {}

        data['user'] = self.__username

        if issuekey is not None:
            data['issueKey'] = issuekey

        if adjust_estimate is not None:
            data['autoAdjustRemaining'] = adjust_estimate

        if night_overtime is not None:
            data['nightOvertime'] = night_overtime

        data['process'] = {
            "id": dzsi.PAIR_WBS_ID_TITLE.get(wbs),
            "technicalDomain": True,
            "haschildren": False,
            "title": wbs,
            "type": ''
        }
        data['projectSites'] = [
            {
                "project": 'PJT:2062',
                "site": 'CHT'
            }
        ]

        now = datetime.now()
        data['started'] = now.strftime("%Y-%m-%dT 9:00")

        data['technologyDomain'] = {
            "id": "3",
            "name": "GPON"
        }

        if time_spent is not None:
            data['timeSpent'] = time_spent
            data['timeSpentSecond'] = int(time_spent)*3600

        url = dzsi.LOGWORK_URL
        r = self._session.post(url, data=json.dumps(data))
        return

test = WrapJira(dzsi.WITS_HTTP, username="nhatanh.nguyen", password="taodeobiet", \
                team='Network')
#test.search_issue_by_username(username="nhatanh.nguyen")
#test.search_issue_by_milestone(milestone='1834')
test.set_issue_status(issuekey='NOSVG-19927')
