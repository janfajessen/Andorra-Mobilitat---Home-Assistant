"""Binary sensors for Andorra Mobilitat."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MobilitatCoordinator
from .sensor import DEVICE_INFO


@dataclass(frozen=True)
class MobilitatBinaryDescription(BinarySensorEntityDescription):
    data_key: str = ""


BINARY_SENSORS: tuple[MobilitatBinaryDescription, ...] = (
    MobilitatBinaryDescription(
        key="any_tall_active",
        name="Talls de circulació actius",
        icon="mdi:sign-direction-plus",
        device_class=BinarySensorDeviceClass.PROBLEM,
        data_key="any_tall_active",
    ),
    MobilitatBinaryDescription(
        key="any_snow_active",
        name="Color Neu actiu (qualsevol carretera)",
        icon="mdi:snowflake-alert",
        device_class=BinarySensorDeviceClass.PROBLEM,
        data_key="any_snow_active",
    ),
    MobilitatBinaryDescription(
        key="prealerta",
        name="Prealerta (taronja / vermella / negra)",
        icon="mdi:car-emergency",
        device_class=BinarySensorDeviceClass.PROBLEM,
        data_key="prealerta",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: MobilitatCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        MobilitatBinarySensor(coordinator, desc) for desc in BINARY_SENSORS
    )


class MobilitatBinarySensor(CoordinatorEntity[MobilitatCoordinator], BinarySensorEntity):
    """Binary sensor reading a boolean key from coordinator data."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MobilitatCoordinator,
        description: MobilitatBinaryDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self._attr_device_info = DEVICE_INFO

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data is None:
            return None
        return bool(self.coordinator.data.get(self.entity_description.data_key))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        if not self.coordinator.data:
            return {}
        key = self.entity_description.data_key
        attrs: dict[str, Any] = {}
        if key == "any_tall_active":
            attrs["talls"] = [i["text"][:200] for i in self.coordinator.data.get("talls", [])]
        elif key == "any_snow_active":
            attrs["carreteres"] = self.coordinator.data.get("snow", {})
        elif key == "prealerta":
            attrs["pitjor_fase"] = self.coordinator.data.get("worst_snow_fase")
            attrs["carreteres"] = self.coordinator.data.get("snow", {})
        return attrs
