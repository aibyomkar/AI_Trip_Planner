import os
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.google_api_key = os.environ.get('GPLACES_API_KEY')
        self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        '''setup all tools for the place search tool'''

        @tool
        def search_attractions(place: str) -> str:
            '''search attractions of a place'''

            try:
                attraction_result = self.google_places_search.google_search_attractions(place)

                if attraction_result:
                    return f'Following are the attractions of {place} as suggested by Google: {attraction_result}'
                    
            except Exception as e:
                tavily_result = self.tavily_search_attractions(place)
                
                return f'Google cannot find the details due to {e}. \nFollowing are the attractions of {place}: {tavily_result}' # Fallback search using tavily in case google places fail
            
            @tool
            def search_restaurants(place: str) -> str:
                '''search restaurants of a place'''

                try:
                    restaurants_result = self.google_places_search.google_search_restaurants(place)

                    if restaurants_result:
                        return f'Following are the restaurants of {place} as suggested by Google: {restaurants_result}'
                except Exception as e:
                    tavily_result = self.tavily_search.tavily_search_restaurants(place)
                    return f'Google cannot find the details due to {e}. \nFollowing are the restaurants of {place}: {tavily_result}' # Fallback search using tavily in case google places fial
                
            @tool
            def search_activities(place: str) -> str:
                '''search activities of a place'''

                try:
                    activity_result = self.google_places_search.google_search_activity(place)

                    if activity_result:
                        return f'Following are the activities of {place} as suggested by Google: {activity_result}'
                except Exception as e:
                    tavily_result = self.tavily_search.tavily_search_activity(place)
                    return f'Google cannot find the details due to {e}. \nFollowing are the activities of {place}: {tavily_result}' # Fallback search using tavily in case google places fail
                
            @tool
            def search_transportation(place: str) -> str:
                '''search transportation of a place'''

                try:
                    transportation_result = self.google_places_search.google_search_transportation(place)

                    if transportation_result:
                        return f'Following are the transportation options in {place} as suggested by Google: {transportation_result}'
                except Exception as e:
                    tavily_result = self.tavily_search.tavily_search_transportation(place)
                    return f'Google cannot find the details due to {e}. \nFollowing are the transportation options in {place}: {tavily_result}' # Fallback search using tavily incase google places fail3
                
            return [search_attractions, search_restaurants, search_activities, search_transportation]