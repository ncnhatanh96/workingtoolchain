import sys
sys.path.append('../src/')

import wrap_jira
test = WrapJira(url=dzsi.WITS_HTTP,
                username="nhatanh.nguyen", password="taodeobiet")
test.create_issue(summary='NhatAnh_testing', fixVersions='TRUE_Universal_WEB_UI_Phrase2',
                    components='DZSV_L2,L3Networks', outwardIssue='NOSVG-20337')
test.clone_issue(issuekey='NOSVG-20237', components='DZSV_L2,L3Networks',
                    fixVersions='TRUE_Universal_WEB_UI_Phrase2')
