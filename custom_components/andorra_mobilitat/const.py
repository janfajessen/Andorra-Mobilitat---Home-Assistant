"""Constants for Andorra Mobilitat integration."""
DOMAIN = "andorra_mobilitat"

CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 5  # minutes

INC_URL = "https://www.mobilitat.ad/totes-incidencies"

EVENT_NEW_INCIDENT = f"{DOMAIN}_nova_incidencia"

ROADS: dict[str, dict] = {
    "CG1": {
        "name": "CG-1 · Andorra - Espanya",
        "keywords": ["CG1", "CG-1"],
    },
    "CG2": {
        "name": "CG-2 · Envalira / Pas de la Casa",
        "keywords": ["CG2", "CG-2", "Envalira", "Pas de la Casa"],
    },
    "CG3": {
        "name": "CG-3 · Ordino / El Serrat",
        "keywords": ["CG3", "CG-3", "Sorteny", "Serrat"],
    },
    "CG4": {
        "name": "CG-4 · La Massana / Pal / Arinsal",
        "keywords": ["CG4", "CG-4", "Pal ", "Arinsal"],
    },
}

SNOW_PHASES = ["ok", "groga", "taronja", "vermella", "negra"]
SNOW_SEVERITY: dict[str, int] = {p: i for i, p in enumerate(SNOW_PHASES)}

INCIDENT_TYPE_NEU    = "neu"
INCIDENT_TYPE_OBRES  = "obres"
INCIDENT_TYPE_TALL   = "tall"
INCIDENT_TYPE_OTHER  = "other"
