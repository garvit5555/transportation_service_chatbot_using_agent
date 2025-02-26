from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests

HERE_API_KEY = "YOUR_HERE_API_KEY"

class TravelRouteInput(BaseModel):
    """Input schema for travel-related tools."""
    source: str = Field(..., description="Starting location for the route.")
    destination: str = Field(..., description="Ending location for the route.")

def get_coordinates(location: str):
    url = f"https://geocode.search.hereapi.com/v1/geocode?q={location}&apiKey={HERE_API_KEY}"
    response = requests.get(url).json()
    if "items" in response and response["items"]:
        position = response["items"][0]["position"]
        return f"{position['lat']},{position['lng']}"
    return None  # If no coordinates found

class TrafficAnalysisTool(BaseTool):
    name: str = "Real-Time Traffic Analysis"
    description: str = "Fetches live traffic conditions and provides a route map using HERE Maps API."
    args_schema: Type[BaseModel] = TravelRouteInput

    def _run(self, source: str, destination: str) -> str:
        try:
            source_coords = get_coordinates(source)
            destination_coords = get_coordinates(destination)

            if not source_coords or not destination_coords:
                return f"Error: Could not find coordinates for {source} or {destination}."

            traffic_url = (
                f"https://traffic.ls.hereapi.com/traffic/6.3/flow.json?"
                f"prox={source_coords}&apiKey={HERE_API_KEY}"
            )
            traffic_response = requests.get(traffic_url).json()

            if "RWS" not in traffic_response:
                return f"No traffic data available for {source} to {destination}."

            traffic_segments = traffic_response["RWS"][0]["RW"]
            traffic_info = []
            for segment in traffic_segments:
                flow_item = segment["FIS"][0]["FI"][0]["CF"][0]
                speed = flow_item["SP"]
                free_flow_speed = flow_item["FF"]
                congestion_level = round((1 - speed / free_flow_speed) * 100, 2)
                traffic_info.append(
                    f"- Speed: {speed} km/h, Free Flow Speed: {free_flow_speed} km/h, Congestion: {congestion_level}%"
                )

            return "Traffic Data:\n" + "\n".join(traffic_info)

        except Exception as e:
            return f"Error fetching traffic data: {str(e)}"
