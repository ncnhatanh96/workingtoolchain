LOGWORK_URL = "http://wits.dzsi.net/rest/dvz/1.0/worklog"
WITS_HTTP = "http://wits.dzsi.net"
WITS_HTTPS = "https://wits.dzsi.net"

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
import json
import utils
class Dzsi():
    def __init__(self):
        self.__dzsi_status_id = {
            'Open': '201',
            'To Do': '11',
            'Make Solution': '21',
            'Review Solution': '31',
            'Implement': '41',
            'Review Code': '51',
            'Closed': '131',
            'Reopened': '191'
        }
        self.__dzsi_workflow = utils.Graph()
        self.__dzsi_workflow.add_vertex('Open')
        self.__dzsi_workflow.add_vertex('To Do')
        self.__dzsi_workflow.add_vertex('Make Solution')
        self.__dzsi_workflow.add_vertex('Review Solution')
        self.__dzsi_workflow.add_vertex('Implement')
        self.__dzsi_workflow.add_vertex('Review Code')
        self.__dzsi_workflow.add_vertex('Closed')
        self.__dzsi_workflow.add_vertex('Reopened')

        self.__dzsi_workflow.add_edge('Open', 'To Do', 1)
        self.__dzsi_workflow.add_edge('Open', 'Closed', 1)
        self.__dzsi_workflow.add_edge('To Do', 'Closed', 1)
        self.__dzsi_workflow.add_edge('To Do', 'Open', 1)
        self.__dzsi_workflow.add_edge('To Do', 'Make Solution', 1)
        self.__dzsi_workflow.add_edge('Make Solution', 'Review Solution', 1)
        self.__dzsi_workflow.add_edge('Make Solution', 'To Do', 1)
        self.__dzsi_workflow.add_edge('Make Solution', 'Closed', 1)
        self.__dzsi_workflow.add_edge('Review Solution', 'Implement', 1)
        self.__dzsi_workflow.add_edge('Review Solution', 'Make Solution', 1)
        self.__dzsi_workflow.add_edge('Review Solution', 'Closed', 1)
        self.__dzsi_workflow.add_edge('Implement', 'Closed', 1)
        self.__dzsi_workflow.add_edge('Implement', 'Review Code', 1)
        self.__dzsi_workflow.add_edge('Implement', 'To Do', 1)
        self.__dzsi_workflow.add_edge('Review Code', 'Closed', 1)
        self.__dzsi_workflow.add_edge('Closed', 'Reopened', 1)
        self.__dzsi_workflow.add_edge('Reopened', 'Closed', 1)
        self.__dzsi_workflow.add_edge('Reopened', 'To Do', 1)

    def get_transitionId_flow(self, cur_status, new_status):
        print(cur_status)
        print(new_status)
        utils.dijkstra(self.__dzsi_workflow, self.__dzsi_workflow.get_vertex(cur_status), \
                    self.__dzsi_workflow.get_vertex(new_status))
        target = self.__dzsi_workflow.get_vertex(new_status)
        path = [target.get_id()]
        utils.shortest(target, path)
        transitionId_flow = []
        for transition in path[::-1]:
            transitionId_flow.append(self.__dzsi_status_id.get(transition))
        return transitionId_flow

