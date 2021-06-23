from datetime import datetime
import json
import dzsi
import wrap_jira
from parse import *

class client():

    def __init__(self, username=None, password=None, team=None):
        self.__jira = wrap_jira.WrapJira(url=dzsi.WITS_HTTP, username=username, password=password, team=team)
        self.__dev_username = ''
        self.__dev_password = ''
        print(json.dumps(self.__jira.get_milestone_list(), indent=4))

    def build_firmware(self):
        return

    def auto_release(self, milestone_list=None):
        issue_table= ''
        device_info_table = ''
        firmware_information_table = ''
        milestone_issuelist = []
        pa_issuekey = ''

        for milestone in milestone_list.split(','):
            #if milestone is in self.__jira.get_milestone_list():
            milestone_issuelist += self.__jira.get_issuelist_by_milestone(milestone=milestone)

        for issue_dict in milestone_issuelist:
            print(issue_dict.get('Summary'))
            if 'Closed' != str(issue_dict.get('Status')):
                print("Warning: Please check Issue {} - Assignee: {} Status {}".format(\
                        issue_dict.get('IssueKey'), issue_dict.get('Assignee'),\
                        issue_dict.get('Status')))
                return

            data_issuelink = self.__jira.get_issuelink(issue_dict.get('IssueLinks'))
            if data_issuelink is None:
                continue
            for issuelink_key in list(data_issuelink.values()):
                issuelink = self.__jira.issue(issuelink_key)
                if 'PreFIXED' == str(issuelink.fields.status):
                    self.__jira.set_issue_status(issuelink, new_status = 'Fixed')
                else:
                    print("Warning: Please check {} status".format(issuelink))
                    #continue
                pa_issuekey = pa_issuekey +',' + issuelink_key
            print(pa_issuekey)
            issue_table += dzsi.FORMAT_HTML_ISSUELIST.format(pa_issuekey,\
                                    issue_dict.get('IssueKey'), issue_dict.get('Summary'))
            pa_issuekey = ''
        print(issue_table)

    def show_milestone(self):
        return

client = client(username="nhatanh.nguyen", password="taodeobiet", team='BIZGW')
#client.auto_release(milestone_list='1846,1803')
