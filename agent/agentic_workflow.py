from utils.model_loader import ModelLoader
from prompt_library.prompt import PromptLibrary
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition

# from tools.weather_info_tool import WeatherInfoTool
# from tools.place_search_tool import PlaceSearchTool
# from tools.expense_calculator_tool import CalculatorTool
# from tools.currency_conversion_tool import currency_conversion_tool


class GraphBuilder():

    def __init__(self):
        pass

    def agent_function(self):
        pass

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)

        graph_builder.add_node('agent', self.agent_function)
        graph_builder.add_node('tools', ToolNode(tools = self.tools))
        graph_builder.add_edge(START, 'agent')
        graph_builder.add_conditional_edges('agent', tools_condition)
        graph_builder.add_edge('tools', 'agent')
        graph_builder.add_edge('agent', END)

    def __call__(self):
        pass