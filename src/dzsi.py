LOGWORK_URL = "http://wits.dzsi.net/rest/dvz/1.0/worklog"
WITS_HTTP = "http://wits.dzsi.net"
WITS_HTTPS = "https://wits.dzsi.net"
MILESTONE_BIZGW_URL = "http://wits.dzsi.net/rest/dcc/1.0/milestone/search?aggregate=true\
                    &asc=true&limit=50&name=[BIZ]&orderBy=status"
MILESTONE_NETWORK_URL = "http://wits.dzsi.net/rest/dcc/1.0/milestone/search?aggregate=true\
                    &asc=true&limit=50&name=Network&name=[BIZ]&orderBy=status"
MILESTONE_PLATFORM_URL = "http://wits.dzsi.net/rest/dcc/1.0/milestone/search?aggregate=true\
                    &asc=true&limit=50&name=Platform&name=[BIZ]&orderBy=status"

PAIR_WBS_ID_TITLE = {
    "Setup development Lab/Verification test" : "N2-3-2-1-1",
    "Development tools and infrastructure" : "N2-3-2-1-2",
    "Implement new feature" : "N2-3-2-1-3",
    "Debugging Defects" : "N2-3-2-1-4",
    "SW Code Review" : "N2-3-2-1-5",
    "Manual Test" : "N2-3-2-1-6",
    "Automatic Test" : "N2-3-2-1-7",
    "Software Release" : "N2-3-2-1-8",
    "SW Development (General)" : "N2-3-2-1-9"
}
FORMAT_HTML_DEVICEINFO = """
    <TR>
        <TH WIDTH="30%">{}</TH>
        <TH WIDTH="30%">{}</TH>
        <TH WIDTH="30%">{}</TH>
    </TR>
"""
FORMAT_HTML_ISSUELIST = """
    <TR>
        <TH WIDTH="30%">{}</TH>
        <TH WIDTH="30%">{}</TH>
        <TH WIDTH="30%">{}</TH>
    </TR>
"""
FORMAT_HTML_FIRMWAREINFORMATION = """
    <TR>
        <TH WIDTH="30%">{}</TH>
        <TH WIDTH="30%">{}</TH>
        <TH WIDTH="30%">{}</TH>
    </TR>
"""
FORMAT_HTML_INSERTLINK = """
    <p><a href="{}">{}</a></p>
"""
FORMAT_HTML_RELEASENOTES = """
<head>
<META http-equiv=Content-Type content="text/html; charset=UTF-8">
<title>Exported from Notepad++</title>
<style type="text/css">
span {
    font-family: 'Courier New';
    font-size: 14pt;
    color: #000000;
}
.sc0 {
}
</style>
</head>
<body><span>
    <div><span>
        Dear all <br>
        This firmware is released for the {} and {} of CHT customer 
        The steps when upgrade firmware for both (ECNT and QTN):<br>
        Step 1: Upgrade firmware ECNT (via web, console,...)<br>
        Step 2: Upgrade firmware QTN (via web or console)<br>
        Step 3: Restore default firmware ECNT (on Web or use prolincecmd restore default)<br>
        Step 4: Restore default firmware QTN (on Web or use command restore_default_g gconfig)<br>
        Dear PA team Please update your test results into PA status columns h580RX-T6 RFP (Type III-vAX) sheet.
    </span></div><br>
    <h5>
        <u>Device info:</u>
    </h5> <br>
    <TABLE BORDER= "1" WIDTH="50%"  CELLPADDING="4" CELLSPACING="3" style="border-collapse: collapse;">
            {}
    </TABLE>
    <h5>
        <u>Firmware:</u>
            <ul>
                <li>{}</li>
            </ul>
    </h5> <br>
    <h5>
        <u>QTN Firmware</u>
			<ul>
                <li>{}</li>
            </ul>
    </h5> <br>
    <h5>
        <u>Firmware ONT version history:</u>
            <ul>
                <li>{}</li>
            </ul>
    </h5> <br>
    <h5>
        <u>Issue List:</u>
    </h5> <br>
   <TABLE BORDER= "1" WIDTH="50%"  CELLPADDING="4" CELLSPACING="3" style="border-collapse: collapse;">
            {}
    </TABLE>
    <h5>
        <u>Firmware Information:</u>
    </h5> <br>
   <TABLE BORDER= "1" WIDTH="50%"  CELLPADDING="4" CELLSPACING="3" style="border-collapse: collapse;">
            {}
    </TABLE>
    <div><span>
        Best Regards<br>
        {}<br>
        {}
    </span></div><br>
</span></body>
"""
import json
import utils
class Dzsi():
    def __init__(self):
        self.__dzsi_RnD_status_id = {
            'Open': '201',
            'To Do': '11',
            'Make Solution': '21',
            'Review Solution': '31',
            'Implement': '41',
            'Review Code': '51',
            'Closed': '131',
            'Reopened': '191'
        }

        self.__dzsi_PA_status_id = {
            'Open': '191',
            'SW Assigned': '181',
            'PreFIXED': '131',
            'Fixed': '121',
            'Reply': '151',
            "Won't Fix": '161',
            'Closed': '141',
            'Killed': '171',
            'Reopened': '81',
            'Later': '11',
        }
        self.__dzsi_RnD_workflow = utils.Graph()
        self.__dzsi_RnD_workflow.add_vertex('Open')
        self.__dzsi_RnD_workflow.add_vertex('To Do')
        self.__dzsi_RnD_workflow.add_vertex('Make Solution')
        self.__dzsi_RnD_workflow.add_vertex('Review Solution')
        self.__dzsi_RnD_workflow.add_vertex('Implement')
        self.__dzsi_RnD_workflow.add_vertex('Review Code')
        self.__dzsi_RnD_workflow.add_vertex('Closed')
        self.__dzsi_RnD_workflow.add_vertex('Reopened')

        self.__dzsi_RnD_workflow.add_edge('Open', 'To Do', 1)
        self.__dzsi_RnD_workflow.add_edge('Open', 'Closed', 1)
        self.__dzsi_RnD_workflow.add_edge('To Do', 'Closed', 1)
        self.__dzsi_RnD_workflow.add_edge('To Do', 'Open', 1)
        self.__dzsi_RnD_workflow.add_edge('To Do', 'Make Solution', 1)
        self.__dzsi_RnD_workflow.add_edge('Make Solution', 'Review Solution', 1)
        self.__dzsi_RnD_workflow.add_edge('Make Solution', 'To Do', 1)
        self.__dzsi_RnD_workflow.add_edge('Make Solution', 'Closed', 1)
        self.__dzsi_RnD_workflow.add_edge('Review Solution', 'Implement', 1)
        self.__dzsi_RnD_workflow.add_edge('Review Solution', 'Make Solution', 1)
        self.__dzsi_RnD_workflow.add_edge('Review Solution', 'Closed', 1)
        self.__dzsi_RnD_workflow.add_edge('Implement', 'Closed', 1)
        self.__dzsi_RnD_workflow.add_edge('Implement', 'Review Code', 1)
        self.__dzsi_RnD_workflow.add_edge('Implement', 'To Do', 1)
        self.__dzsi_RnD_workflow.add_edge('Review Code', 'Closed', 1)
        self.__dzsi_RnD_workflow.add_edge('Closed', 'Reopened', 1)
        self.__dzsi_RnD_workflow.add_edge('Reopened', 'Closed', 1)
        self.__dzsi_RnD_workflow.add_edge('Reopened', 'To Do', 1)

        self.__dzsi_PA_workflow = utils.Graph()
        self.__dzsi_PA_workflow.add_vertex('Open')
        self.__dzsi_PA_workflow.add_vertex('SW Assigned')
        self.__dzsi_PA_workflow.add_vertex('PreFIXED')
        self.__dzsi_PA_workflow.add_vertex('Fixed')
        self.__dzsi_PA_workflow.add_vertex('Reply')
        self.__dzsi_PA_workflow.add_vertex("Won't Fix")
        self.__dzsi_PA_workflow.add_vertex('Closed')
        self.__dzsi_PA_workflow.add_vertex('Killed')
        self.__dzsi_PA_workflow.add_vertex('Reopened')

        self.__dzsi_PA_workflow.add_edge('Open', 'Later', 1)
        self.__dzsi_PA_workflow.add_edge('Open', 'Closed', 1)
        self.__dzsi_PA_workflow.add_edge('Open', 'SW Assigned', 1)
        self.__dzsi_PA_workflow.add_edge('Open', 'Fixed', 1)
        self.__dzsi_PA_workflow.add_edge('SW Assigned', 'PreFIXED', 1)
        self.__dzsi_PA_workflow.add_edge('SW Assigned', 'Reply', 1)
        self.__dzsi_PA_workflow.add_edge('SW Assigned', 'Open', 1)
        self.__dzsi_PA_workflow.add_edge('Reply', "Won't Fix", 1)
        self.__dzsi_PA_workflow.add_edge('Reply', "Killed", 1)
        self.__dzsi_PA_workflow.add_edge('Reply', "SW Assigned", 1)
        self.__dzsi_PA_workflow.add_edge("Won't Fix", "Reopened", 1)
        self.__dzsi_PA_workflow.add_edge("Closed", "Reopened", 1)
        self.__dzsi_PA_workflow.add_edge("Killed", "Reopened", 1)
        self.__dzsi_PA_workflow.add_edge("Reopened", "SW Assigned", 1)
        self.__dzsi_PA_workflow.add_edge("Reopened", "Closed", 1)
        self.__dzsi_PA_workflow.add_edge("Later", "SW Assigned", 1)
        self.__dzsi_PA_workflow.add_edge("Later", "Closed", 1)
        self.__dzsi_PA_workflow.add_edge("Later", "Open", 1)

    def get_transitionId_flow(self, cur_status, new_status):
        if cur_status and new_status in self.__dzsi_RnD_status_id:
            utils.dijkstra(self.__dzsi_RnD_workflow, self.__dzsi_RnD_workflow.get_vertex(cur_status), \
                        self.__dzsi_RnD_workflow.get_vertex(new_status))
            target = self.__dzsi_RnD_workflow.get_vertex(new_status)
            path = [target.get_id()]
            utils.shortest(target, path)
            transitionId_flow = []
            for transition in path[::-1]:
                transitionId_flow.append(self.__dzsi_RnD_status_id.get(transition))
            return transitionId_flow
        else:
            utils.dijkstra(self.__dzsi_PA_workflow, self.__dzsi_PA_workflow.get_vertex(cur_status), \
                        self.__dzsi_PA_workflow.get_vertex(new_status))
            target = self.__dzsi_PA_workflow.get_vertex(new_status)
            path = [target.get_id()]
            utils.shortest(target, path)
            transitionId_flow = []
            for transition in path[::-1]:
                transitionId_flow.append(self.__dzsi_PA_status_id.get(transition))
            return transitionId_flow

