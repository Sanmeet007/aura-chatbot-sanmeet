from typing import Dict, Any
import json


class FarmContextBuilder:
    def __init__(
        self,
        data_path: str,
    ) -> None:
        with open(data_path, "r") as fd:
            self.FARM_DATA: Dict[str, Any] = json.load(fd)

    def get_farm(self, farm_id: str) -> Dict[str, Any]:
        farms = self.FARM_DATA.get("farms", [])

        farm = next((f for f in farms if f.get("farmId") == farm_id), None)

        if not farm:
            raise ValueError(f"Farm with id '{farm_id}' not found")

        return farm

    def build_context(self, farm_id: str) -> str:
        farm = self.get_farm(farm_id)
        return self._format_farm_data(farm)

    def _format_farm_data(self, farm: dict) -> str:
        sensors = farm.get("sensors", {})

        return f"""
Farm ID: {farm.get('farmId')}
Crop: {farm.get('currentCrop')} ({farm.get('variety')})
Growth Stage: {farm.get('growthStage')}
Days After Transplant: {farm.get('daysAfterTransplant')}

Sensor Readings:
- Temperature: {sensors.get('temperature')} °C
- Humidity: {sensors.get('humidity')} %
- EC: {sensors.get('ec')} mS/cm
- pH: {sensors.get('ph')}
- Light (PPFD): {sensors.get('ppfd')}
- CO₂: {sensors.get('co2')} ppm
- Water Temp: {sensors.get('waterTemp')} °C

Notes:
{farm.get('notes')}
""".strip()


farm_ctx_builder = FarmContextBuilder("./data/sample_farm_data.json")


def build_farm_context(inputs):
    farm_id = inputs.get("farm_id")
    if farm_id:
        return farm_ctx_builder.build_context(farm_id)
    return "No farm sensor data connected."
