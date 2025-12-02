# # react (reasoning and action agentic ai workflow)

# from utils.model_loader import ModelLoader
# from prompt_library.prompt import SYSTEM_PROMPT
# from langgraph.graph import StateGraph, MessagesState, END, START
# from langgraph.prebuilt import ToolNode, tools_condition
# from tools.weather_info_tool import WeatherInfoTool
# from tools.place_search_tool import PlaceSearchTool
# from tools.expense_calculator_tool import CalculatorTool
# from tools.currency_conversion_tool import CurrencyConverterTool

# class GraphBuilder():
#     def __init__(self, model_provider: str = "groq"):  # ✅ Fixed: proper __init__
#         self.model_loader = ModelLoader(model_provider=model_provider)
#         self.llm = self.model_loader.load_llm()
        
#         self.tools = []
        
#         # Initialize tool classes
#         self.weather_tools = WeatherInfoTool()
#         self.place_search_tools = PlaceSearchTool()
#         self.calculator_tools = CalculatorTool()
#         self.currency_converter_tools = CurrencyConverterTool()
        
#         # ✅ Safe way to extend tools - won't crash if any tool_list is None
#         tool_lists = [
#             self.weather_tools.weather_tool_list,
#             self.place_search_tools.place_search_tool_list,
#             self.calculator_tools.calculator_tool_list,
#             self.currency_converter_tools.currency_converter_tool_list
#         ]
        
#         # Add tools safely
#         for tool_list in tool_lists:
#             if tool_list:  # Only add if not None and not empty
#                 self.tools.extend(tool_list)
                
#         # Optional: Print debug info
#         print(f"✅ Total tools loaded: {len(self.tools)}")
        
#         self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
#         self.graph = None
#         self.system_prompt = SYSTEM_PROMPT
    
#     def agent_function(self, state: MessagesState):
#         """Main agent function"""
#         user_question = state["messages"]
#         input_question = [self.system_prompt] + user_question
#         response = self.llm_with_tools.invoke(input_question)
#         return {"messages": [response]}
    
#     def build_graph(self):
#         graph_builder = StateGraph(MessagesState)
#         graph_builder.add_node("agent", self.agent_function)
#         graph_builder.add_node("tools", ToolNode(tools=self.tools))
#         graph_builder.add_edge(START, "agent")
#         graph_builder.add_conditional_edges("agent", tools_condition)
#         graph_builder.add_edge("tools", "agent")
#         graph_builder.add_edge("agent", END)
#         self.graph = graph_builder.compile()
#         return self.graph
        
#     def __call__(self):  # ✅ Fixed: proper __call__
#         return self.build_graph()
























# agentic_workflow.py (patched)
# react (reasoning and action agentic ai workflow)
from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

def _normalize_input_messages(raw_msgs):
    """
    Accept:
      - a MessagesState-like object (support dict-like access and attribute access)
      - list of strings
      - list of dicts (with keys 'content' or 'message')
      - single string
    Return: list[str]
    """
    if raw_msgs is None:
        return []

    # If it's a MessagesState or object supporting dict access like state["messages"]
    try:
        # Try mapping common MessageState shapes
        if hasattr(raw_msgs, "__getitem__") and "messages" in getattr(raw_msgs, "__dict__", {}):
            # fallback if object has attribute messages in __dict__
            raw = getattr(raw_msgs, "messages")
            if raw is not None:
                raw_msgs = raw
    except Exception:
        pass

    # If it's a dict with 'messages' key
    if isinstance(raw_msgs, dict) and "messages" in raw_msgs:
        raw_msgs = raw_msgs["messages"]

    # If it's MessagesState object that supports subscription like state["messages"]
    try:
        # many MessageState implementations support __getitem__
        maybe = raw_msgs["messages"] if isinstance(raw_msgs, dict) and "messages" in raw_msgs else raw_msgs
    except Exception:
        maybe = raw_msgs

    # If someone passed the whole request with key 'query'
    if isinstance(maybe, dict) and "query" in maybe and isinstance(maybe["query"], str):
        return [maybe["query"]]

    # If single string
    if isinstance(maybe, str):
        return [maybe]

    # If list-like
    if hasattr(maybe, "__iter__"):
        out = []
        for m in maybe:
            if m is None:
                continue
            if isinstance(m, str):
                out.append(m)
            elif isinstance(m, dict):
                # common shapes: {"content": "..."} or {"message": "..."}
                if "content" in m and isinstance(m["content"], str):
                    out.append(m["content"])
                elif "message" in m and isinstance(m["message"], str):
                    out.append(m["message"])
                else:
                    out.append(str(m))
            else:
                # object with .content attribute (SDK message objects)
                content = getattr(m, "content", None) or getattr(m, "text", None) or getattr(m, "message", None)
                if isinstance(content, str):
                    out.append(content)
                else:
                    out.append(str(m))
        return out

    # Fallback to string repr
    return [str(maybe)]

def _normalize_output_to_string(resp):
    """
    Convert various SDK response shapes into a plain string (safe to JSON serialize).
    """
    if resp is None:
        return ""
    # If dict with 'messages' or 'answer' or 'plan'
    if isinstance(resp, dict):
        if "answer" in resp and isinstance(resp["answer"], str):
            return resp["answer"]
        if "plan" in resp:
            # return JSON-dumpable representation (string form)
            try:
                import json
                return json.dumps(resp["plan"], default=str, ensure_ascii=False)
            except Exception:
                return str(resp["plan"])
        if "messages" in resp:
            last = resp["messages"][-1]
            # try common shapes
            if isinstance(last, dict) and "content" in last:
                return last["content"]
            # if SDK message object inside dict
            content = getattr(last, "content", None) or getattr(last, "text", None)
            if isinstance(content, str):
                return content
            return str(last)
        # fallback to stringified dict
        try:
            import json
            return json.dumps(resp, default=str, ensure_ascii=False)
        except Exception:
            return str(resp)

    # If it's a list, join
    if isinstance(resp, (list, tuple)):
        try:
            return "\n".join([_normalize_output_to_string(x) for x in resp])
        except Exception:
            return str(resp)

    # SDK object with .content or .text
    content = getattr(resp, "content", None) or getattr(resp, "text", None)
    if isinstance(content, str):
        return content

    # fallback
    return str(resp)


class GraphBuilder():
    def __init__(self, model_provider: str = "groq"):
        # load model via your existing ModelLoader
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()

        self.tools = []

        # Initialize tool classes
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()

        # Safe way to extend tools - won't crash if any tool_list is None
        tool_lists = [
            getattr(self.weather_tools, "weather_tool_list", None),
            getattr(self.place_search_tools, "place_search_tool_list", None),
            getattr(self.calculator_tools, "calculator_tool_list", None),
            getattr(self.currency_converter_tools, "currency_converter_tool_list", None),
        ]

        for tool_list in tool_lists:
            if tool_list:
                self.tools.extend(tool_list)

        print(f"✅ Total tools loaded: {len(self.tools)}")

        # bind tools if available; guard if llm doesn't have bind_tools
        if hasattr(self.llm, "bind_tools"):
            try:
                self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
            except Exception as e:
                # fallback to plain llm if binding fails
                print("⚠️ Warning: llm.bind_tools() failed, continuing with plain LLM:", e)
                self.llm_with_tools = self.llm
        else:
            self.llm_with_tools = self.llm

        self.graph = None
        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessagesState):
        """
        Main agent function. Normalizes incoming state to strings, calls the LLM (with tools),
        and returns a standardized messages dict with string content.
        """
        try:
            # Try many ways to extract messages from 'state'
            # Accept MessagesState, dict, list, or single string.
            raw_user_msgs = None
            try:
                # MessagesState typically supports subscription like state["messages"]
                raw_user_msgs = state["messages"]
            except Exception:
                # maybe dict-like or object with attribute
                if isinstance(state, dict) and "messages" in state:
                    raw_user_msgs = state["messages"]
                elif hasattr(state, "messages"):
                    raw_user_msgs = getattr(state, "messages")
                else:
                    raw_user_msgs = state

            user_messages = _normalize_input_messages(raw_user_msgs)

            # Prepend system prompt
            input_for_llm = [self.system_prompt] + user_messages

            # Invoke the LLM (with tools) - many LLMs accept a list of strings
            if hasattr(self.llm_with_tools, "invoke"):
                resp = self.llm_with_tools.invoke(input_for_llm)
            elif hasattr(self.llm_with_tools, "call"):
                resp = self.llm_with_tools.call(input_for_llm)
            else:
                # Fallback: try calling the llm directly if it's callable
                try:
                    resp = self.llm_with_tools(input_for_llm)
                except Exception as e:
                    resp = None
                    print("❌ LLM invocation failed:", e)

            # Normalize output into a simple string payload
            out_txt = _normalize_output_to_string(resp)

            # Return messages shaped as a list of simple dicts (safe to serialize)
            return {"messages": [{"content": out_txt}]}

        except Exception as e:
            # Ensure any internal error returns a safe structure and logs
            print("❌ agent_function internal error:", e)
            import traceback as _tb
            print(_tb.format_exc())
            return {"messages": [{"content": f"Agent internal error: {e}"}]}

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)
        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()
