import json
import dzsi
from jira import JIRA
from datetime import datetime

class WrapJira(JIRA):

    def __INIT__(self, url, username, password):
        JIRA.__init__(self, server=url, basic_auth=(username, password))
        self.__username = username
        self.__password = password

    def add_worklog(self, issue=None, timeSpent=None, timeSpentSecond=None, adjustEstimate=True,
                    newEstimate=None, reduceBy=None, started=None, projectId=None,
                    site=None, domainId=None, nightOvertime=False, WBS=None):
        data = {}

        data['user'] = self.__dzsi_username

        if issue is not None:
            data['issueKey'] = issue

        if adjustEstimate is not None:
            data['autoAdjustRemaining'] = adjustEstimate

        if nightOvertime is not None:
            data['nightOvertime'] = nightOvertime

        data['process'] = {
            "id": dzsi.PAIR_WBS_ID_TITLE.get(WBS),
            "technicalDomain": True,
            "haschildren": False,
            "title": WBS,
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

        if timeSpent is not None:
            data['timeSpent'] = timeSpent

        if timeSpentSecond is not None:
            data['timeSpentSecond'] = timeSpentSecond

        url = dzsi.LOGWORK_URL
        r = self._session.post(url, data=json.dumps(data))
        return
