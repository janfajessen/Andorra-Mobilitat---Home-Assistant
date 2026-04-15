"""DataUpdateCoordinator for Andorra Mobilitat."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import aiohttp
from bs4 import BeautifulSoup

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    INC_URL,
    INCIDENT_TYPE_NEU,
    INCIDENT_TYPE_OBRES,
    INCIDENT_TYPE_TALL,
    INCIDENT_TYPE_OTHER,
    ROADS,
    SNOW_SEVERITY,
)

_LOGGER = logging.getLogger(__name__)

EVENT_NEW_INCIDENT = f"{DOMAIN}_nova_incidencia"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; HomeAssistant/2026.2; "
        "Andorra Mobilitat Integration)"
    ),
    "Accept-Language": "ca,es;q=0.9",
}


class MobilitatCoordinator(DataUpdateCoordinator):
    """Coordinator: fetch & parse mobilitat.ad every N minutes."""

    def __init__(self, hass: HomeAssistant, update_interval_minutes: int) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval_minutes),
        )
        self._known_incident_texts: set[str] = set()

    async def _async_update_data(self) -> dict:
        """Fetch data from mobilitat.ad."""
        try:
            async with aiohttp.ClientSession(headers=HEADERS) as session:
                async with session.get(
                    INC_URL, timeout=aiohttp.ClientTimeout(total=20)
                ) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"HTTP {resp.status} from mobilitat.ad")
                    html = await resp.text(encoding="utf-8", errors="replace")
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Connection error: {err}") from err

        # BS4 parsing is CPU-bound — run in executor to avoid blocking the event loop
        data = await self.hass.async_add_executor_job(_parse_page, html)

        # Fire HA events for new incidents
        current_texts = {i["text"] for i in data["incidents"]}
        new_texts = current_texts - self._known_incident_texts
        if self._known_incident_texts:  # skip on first load
            for inc in data["incidents"]:
                if inc["text"] in new_texts:
                    self.hass.bus.async_fire(
                        EVENT_NEW_INCIDENT,
                        {
                            "tipus": inc["type"],
                            "text":  inc["text"][:300],
                        },
                    )
                    _LOGGER.info(
                        "Nova incidència detectada [%s]: %s",
                        inc["type"],
                        inc["text"][:80],
                    )
        self._known_incident_texts = current_texts

        return data


# ─────────────────────────────────────────────────────
# Parsing helpers — pure functions, safe to run in
# a thread via async_add_executor_job
# ─────────────────────────────────────────────────────

def _detect_type(row_text: str, img_alts: list[str]) -> str:
    """Classify an incident row."""
    combined = (row_text + " " + " ".join(img_alts)).lower()

    if any(x in combined for x in [
        "fase groga", "fase taronja", "fase vermell", "fase negra",
        "color de la neu", "pneumàtics especials", "cadenes",
    ]):
        return INCIDENT_TYPE_NEU
    if any(x in combined for x in ["obra", "embelliment", "reasfaltat", "paviment"]):
        return INCIDENT_TYPE_OBRES
    if any(x in combined for x in ["tall", "manifestaci", "tancament", "restrict"]):
        return INCIDENT_TYPE_TALL
    return INCIDENT_TYPE_OTHER


def _parse_andorra_incidents(soup: BeautifulSoup) -> list[dict]:
    """Extract Andorra-specific incident rows from the page."""
    andorra_table = None
    for table in soup.find_all("table"):
        prev = table.find_previous(["h2", "h3", "p", "strong"])
        if prev and "andorr" in prev.get_text().lower():
            andorra_table = table
            break

    if andorra_table is None:
        andorra_table = soup.find("table")

    if andorra_table is None:
        _LOGGER.warning("andorra_mobilitat: no table found on page")
        return []

    incidents: list[dict] = []
    for row in andorra_table.find_all("tr"):
        cells = row.find_all("td")
        if not cells:
            continue

        text = cells[-1].get_text(separator="\n").strip()
        if len(text) < 5:
            continue

        img_alts = [
            (img.get("alt", "") + " " + img.get("src", ""))
            for img in row.find_all("img")
        ]
        inc_type = _detect_type(text, img_alts)
        incidents.append({"text": text, "type": inc_type})

    return incidents


def _parse_snow_colors(incidents: list[dict]) -> dict[str, str]:
    """Return {road_id: fase} for each configured road."""
    result: dict[str, str] = {road_id: "ok" for road_id in ROADS}

    for inc in incidents:
        if inc["type"] != INCIDENT_TYPE_NEU:
            continue
        text_upper = inc["text"].upper()

        if "NEGRA" in text_upper:
            fase = "negra"
        elif "VERMELL" in text_upper:
            fase = "vermella"
        elif "TARONJA" in text_upper:
            fase = "taronja"
        elif "GROGA" in text_upper:
            fase = "groga"
        else:
            continue

        for road_id, road_cfg in ROADS.items():
            for kw in road_cfg["keywords"]:
                if kw.upper() in text_upper:
                    current = result[road_id]
                    if SNOW_SEVERITY[fase] > SNOW_SEVERITY[current]:
                        result[road_id] = fase
                    break

    return result


def _parse_page(html: str) -> dict:
    """Full parse — runs in executor thread, must be pure/synchronous."""
    soup = BeautifulSoup(html, "html.parser")
    incidents = _parse_andorra_incidents(soup)

    snow = _parse_snow_colors(incidents)

    talls  = [i for i in incidents if i["type"] == INCIDENT_TYPE_TALL]
    obres  = [i for i in incidents if i["type"] == INCIDENT_TYPE_OBRES]
    neu    = [i for i in incidents if i["type"] == INCIDENT_TYPE_NEU]
    other  = [i for i in incidents if i["type"] == INCIDENT_TYPE_OTHER]

    max_severity = max((SNOW_SEVERITY[v] for v in snow.values()), default=0)
    worst_label  = next(
        (k for k, v in SNOW_SEVERITY.items() if v == max_severity), "ok"
    )

    return {
        "incidents":        incidents,
        "incidents_total":  len(incidents),
        "talls":            talls,
        "talls_count":      len(talls),
        "obres":            obres,
        "obres_count":      len(obres),
        "neu_incidents":    neu,
        "other":            other,
        "snow":             snow,
        "worst_snow_fase":  worst_label,
        "any_snow_active":  any(v != "ok" for v in snow.values()),
        "any_tall_active":  len(talls) > 0,
        "prealerta":        max_severity >= SNOW_SEVERITY.get("taronja", 2),
        "last_update":      datetime.now(timezone.utc),
    }
    