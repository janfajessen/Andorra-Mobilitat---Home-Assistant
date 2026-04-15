"""Sensors for Andorra Mobilitat."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ROADS
from .coordinator import MobilitatCoordinator

DEVICE_INFO = {
    "identifiers": {(DOMAIN, DOMAIN)},
    "name": "Andorra Mobilitat",
    "manufacturer": "Govern d'Andorra",
    "model": "Departament de Mobilitat",
    "configuration_url": "https://www.mobilitat.ad",
}


@dataclass(frozen=True)
class MobilitatSensorDescription(SensorEntityDescription):
    """Extended description for Andorra Mobilitat sensors."""
    data_key: str = ""
    extra_attrs_key: str | None = None


STATIC_SENSORS: tuple[MobilitatSensorDescription, ...] = (
    MobilitatSensorDescription(
        key="incidents_total",
        name="Incidències Andorra",
        icon="mdi:alert-circle-outline",
        native_unit_of_measurement="incidències",
        data_key="incidents_total",
        extra_attrs_key="incidents",
    ),
    MobilitatSensorDescription(
        key="talls_count",
        name="Talls de circulació",
        icon="mdi:sign-caution",
        native_unit_of_measurement="talls",
        data_key="talls_count",
        extra_attrs_key="talls",
    ),
    MobilitatSensorDescription(
        key="obres_count",
        name="Obres en carretera",
        icon="mdi:shovel",
        native_unit_of_measurement="obres",
        data_key="obres_count",
        extra_attrs_key="obres",
    ),
    MobilitatSensorDescription(
        key="worst_snow_fase",
        name="Fase neu (pitjor activa)",
        icon="mdi:snowflake-alert",
        data_key="worst_snow_fase",
    ),
    MobilitatSensorDescription(
        key="last_update",
        name="Última actualització",
        icon="mdi:clock-outline",
        device_class=SensorDeviceClass.TIMESTAMP,
        data_key="last_update",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: MobilitatCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []

    # Static sensors
    for desc in STATIC_SENSORS:
        entities.append(MobilitatStaticSensor(coordinator, desc))

    # One snow-color sensor per road
    for road_id, road_cfg in ROADS.items():
        entities.append(MobilitatSnowSensor(coordinator, road_id, road_cfg["name"]))

    async_add_entities(entities)


# ─── Base ───────────────────────────────────────────────────

class MobilitatBaseSensor(CoordinatorEntity[MobilitatCoordinator], SensorEntity):
    """Base class with common attributes."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: MobilitatCoordinator, unique_suffix: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{unique_suffix}"
        self._attr_device_info = DEVICE_INFO


# ─── Static sensors ─────────────────────────────────────────

class MobilitatStaticSensor(MobilitatBaseSensor):
    """Generic sensor reading a key from coordinator data."""

    entity_description: MobilitatSensorDescription

    def __init__(
        self,
        coordinator: MobilitatCoordinator,
        description: MobilitatSensorDescription,
    ) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        if self.coordinator.data is None:
            return None
        val = self.coordinator.data.get(self.entity_description.data_key)
        return val

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        attrs: dict[str, Any] = {}
        if not self.coordinator.data:
            return attrs
        key = self.entity_description.extra_attrs_key
        if not key:
            return attrs
        raw = self.coordinator.data.get(key, [])
        if not raw:
            return attrs
        if isinstance(raw[0], dict):
            attrs["total"] = len(raw)
            attrs["llista"] = [i["text"][:250] for i in raw]
            attrs["tipus"]  = [i["type"] for i in raw]
        else:
            attrs["llista"] = raw
        return attrs


# ─── Snow color sensor ───────────────────────────────────────

class MobilitatSnowSensor(MobilitatBaseSensor):
    """Snow color phase sensor for a specific road."""

    _attr_icon = "mdi:highway"

    def __init__(
        self,
        coordinator: MobilitatCoordinator,
        road_id: str,
        road_name: str,
    ) -> None:
        super().__init__(coordinator, f"snow_{road_id.lower()}")
        self._road_id   = road_id
        self._road_name = road_name
        self._attr_name = f"Color Neu {road_id}"

    @property
    def native_value(self) -> str | None:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data["snow"].get(self._road_id, "ok")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        fase     = self.native_value or "ok"
        road_cfg = ROADS.get(self._road_id, {})
        attrs: dict[str, Any] = {
            "carretera": road_cfg.get("name", self._road_id),
            "fase":      fase,
        }
        if self.coordinator.data and fase != "ok":
            for inc in self.coordinator.data.get("neu_incidents", []):
                kws = ROADS[self._road_id]["keywords"]
                if any(k.upper() in inc["text"].upper() for k in kws):
                    attrs["detall"] = inc["text"][:300]
                    break
        return attrs
