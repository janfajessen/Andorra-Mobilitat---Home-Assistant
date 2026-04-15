<div align="center">

# Andorra Mobilitat <br> Home Assistant Integration

<img src="brands/logo@2x.png" width="450"/>

![Version](https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge)
![HA](https://img.shields.io/badge/Home%20Assistant-2024.1+-orange?style=for-the-badge&logo=home-assistant)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python)
![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/janfajessen)
[![Patreon](https://img.shields.io/badge/Patreon-Support-red?style=for-the-badge&logo=patreon)](https://www.patreon.com/janfajessen)
<!--[![Ko-Fi](https://img.shields.io/badge/Ko--Fi-Support-teal?style=for-the-badge&logo=ko-fi)](https://ko-fi.com/janfajessen)
[![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Support-pink?style=for-the-badge&logo=githubsponsors)](https://github.com/sponsors/janfajessen)
[![PayPal](https://img.shields.io/badge/PayPal-Donate-blue?style=for-the-badge&logo=paypal)](https://paypal.me/janfajessen)-->
</div>

<details>
<summary>🇪🇸 Español</summary>

## Andorra Mobilitat — Componente personalizado para Home Assistant

Integración no oficial que lee en tiempo real los datos de **mobilitat.ad** (Govern d'Andorra).
No se necesita ninguna clave de API ni registro.

### ⚡ Instalación rápida

**Opción A — Manual**
1. Copia la carpeta `custom_components/andorra_mobilitat/` a la carpeta `custom_components/` de tu HA.
2. Reinicia HA.
3. Ve a **Configuración → Integraciones → + Añadir integración** y busca **Andorra Mobilitat**.
4. Introduce el intervalo de actualización (por defecto 5 minutos) y acepta.
<img src="brands/icon@2x.png" width="100"/>

**Opción B — HACS**
Añade el repositorio como custom repository en HACS e instala desde allí.

### 🌡️ Entidades creadas

**Sensores**

| Entity ID | Descripción | Unidad |
|-----------|-------------|--------|
| `sensor.andorra_mobilitat_incidencies_andorra` | Total incidencias activas | incidències |
| `sensor.andorra_mobilitat_talls_de_circulacio` | Número de cortes activos | talls |
| `sensor.andorra_mobilitat_obres_en_carretera` | Número de obras activas | obres |
| `sensor.andorra_mobilitat_fase_neu_pitjor_activa` | Fase de nieve más grave ahora | texto |
| `sensor.andorra_mobilitat_color_neu_cg1` | Color nieve CG-1 (Andorra-España) | texto |
| `sensor.andorra_mobilitat_color_neu_cg2` | Color nieve CG-2 (Envalira/Pas) | texto |
| `sensor.andorra_mobilitat_color_neu_cg3` | Color nieve CG-3 (Ordino/Serrat) | texto |
| `sensor.andorra_mobilitat_color_neu_cg4` | Color nieve CG-4 (Massana/Pal) | texto |

Valores posibles de los sensores de nieve: `ok` · `groga` · `taronja` · `vermella` · `negra`

**Binary Sensors**

| Entity ID | ON cuando... |
|-----------|-------------|
| `binary_sensor.andorra_mobilitat_talls_de_circulacio_actius` | Alguna carretera cortada |
| `binary_sensor.andorra_mobilitat_color_neu_actiu_qualsevol_carretera` | Cualquier CG en fase activa |
| `binary_sensor.andorra_mobilitat_prealerta_taronja_vermella_negra` | CG en fase naranja / roja / negra |

### 🤖 Ejemplos de automatizaciones

**Notificación cuando CG-2 pasa a fase roja o negra**
```yaml
automation:
  - alias: "Alerta CG-2 Envalira fase grave"
    trigger:
      - platform: state
        entity_id: sensor.andorra_mobilitat_color_neu_cg2
        to: ["vermella", "negra"]
    action:
      - service: notify.mobile_app_mi_telefono
        data:
          title: "⛔ CG-2 Envalira"
          message: >
            Fase {{ states('sensor.andorra_mobilitat_color_neu_cg2') | upper }}
            activada. Comprueba las condiciones antes de salir.
```

**Notificación de cualquier corte nuevo**
```yaml
automation:
  - alias: "Corte de circulación nuevo"
    trigger:
      - platform: state
        entity_id: binary_sensor.andorra_mobilitat_talls_de_circulacio_actius
        to: "on"
    action:
      - service: notify.mobile_app_mi_telefono
        data:
          title: "🚧 Corte de circulación Andorra"
          message: >
            Hay {{ states('sensor.andorra_mobilitat_talls_de_circulacio') }} corte(s) activo(s).
            {% set talls = state_attr('sensor.andorra_mobilitat_talls_de_circulacio','llista') %}
            {% if talls %}{{ talls[0][:100] }}{% endif %}
```

</details>

<details>
<summary>🇫🇷 Français</summary>

## Andorra Mobilitat — Composant personnalisé pour Home Assistant

Intégration non officielle qui lit en temps réel les données de **mobilitat.ad** (Govern d'Andorra).
Aucune clé API ni inscription requise.

### ⚡ Installation rapide

**Option A — Manuelle**
1. Copiez le dossier `custom_components/andorra_mobilitat/` dans le dossier `custom_components/` de votre HA.
2. Redémarrez HA.
3. Allez dans **Configuration → Intégrations → + Ajouter une intégration** et cherchez **Andorra Mobilitat**.
4. Entrez l'intervalle de mise à jour (5 minutes par défaut) et validez.
<img src="brands/icon@2x.png" width="100"/>

**Option B — HACS**
Ajoutez le dépôt comme custom repository dans HACS et installez depuis là.

### 🌡️ Entités créées

**Capteurs**

| Entity ID | Description | Unité |
|-----------|-------------|-------|
| `sensor.andorra_mobilitat_incidencies_andorra` | Total incidents actifs | incidències |
| `sensor.andorra_mobilitat_talls_de_circulacio` | Nombre de coupures actives | talls |
| `sensor.andorra_mobilitat_obres_en_carretera` | Nombre de travaux actifs | obres |
| `sensor.andorra_mobilitat_fase_neu_pitjor_activa` | Phase neige la plus grave | texte |
| `sensor.andorra_mobilitat_color_neu_cg1` | Couleur neige CG-1 (Andorre-Espagne) | texte |
| `sensor.andorra_mobilitat_color_neu_cg2` | Couleur neige CG-2 (Envalira/Pas) | texte |
| `sensor.andorra_mobilitat_color_neu_cg3` | Couleur neige CG-3 (Ordino/Serrat) | texte |
| `sensor.andorra_mobilitat_color_neu_cg4` | Couleur neige CG-4 (Massana/Pal) | texte |

Valeurs possibles des capteurs neige : `ok` · `groga` · `taronja` · `vermella` · `negra`

**Capteurs binaires**

| Entity ID | ON quand... |
|-----------|------------|
| `binary_sensor.andorra_mobilitat_talls_de_circulacio_actius` | Une route est coupée |
| `binary_sensor.andorra_mobilitat_color_neu_actiu_qualsevol_carretera` | N'importe quelle CG en phase active |
| `binary_sensor.andorra_mobilitat_prealerta_taronja_vermella_negra` | CG en phase orange / rouge / noire |

### 🤖 Exemple d'automatisation

**Notification quand CG-2 passe en phase rouge ou noire**
```yaml
automation:
  - alias: "Alerte CG-2 Envalira phase grave"
    trigger:
      - platform: state
        entity_id: sensor.andorra_mobilitat_color_neu_cg2
        to: ["vermella", "negra"]
    action:
      - service: notify.mobile_app_mon_telephone
        data:
          title: "⛔ CG-2 Envalira"
          message: >
            Phase {{ states('sensor.andorra_mobilitat_color_neu_cg2') | upper }}
            activée. Vérifiez les conditions avant de partir.
```

</details>

<details>
<summary>🇬🇧 English</summary>

## Andorra Mobilitat — Custom Component for Home Assistant

Unofficial integration that reads real-time data from **mobilitat.ad** (Govern d'Andorra).
No API key or registration required.

### ⚡ Quick install

**Option A — Manual**
1. Copy the `custom_components/andorra_mobilitat/` folder to the `custom_components/` folder of your HA.
2. Restart HA.
3. Go to **Settings → Integrations → + Add integration** and search for **Andorra Mobilitat**.
4. Enter the update interval (default 5 minutes) and confirm.
<img src="brands/icon@2x.png" width="100"/>

**Option B — HACS**
Add the repository as a custom repository in HACS and install from there.

### 🌡️ Created entities

**Sensors**

| Entity ID | Description | Unit |
|-----------|-------------|------|
| `sensor.andorra_mobilitat_incidencies_andorra` | Total active incidents | incidències |
| `sensor.andorra_mobilitat_talls_de_circulacio` | Number of active road closures | talls |
| `sensor.andorra_mobilitat_obres_en_carretera` | Number of active roadworks | obres |
| `sensor.andorra_mobilitat_fase_neu_pitjor_activa` | Worst active snow phase | text |
| `sensor.andorra_mobilitat_color_neu_cg1` | Snow color CG-1 (Andorra-Spain) | text |
| `sensor.andorra_mobilitat_color_neu_cg2` | Snow color CG-2 (Envalira/Pas) | text |
| `sensor.andorra_mobilitat_color_neu_cg3` | Snow color CG-3 (Ordino/Serrat) | text |
| `sensor.andorra_mobilitat_color_neu_cg4` | Snow color CG-4 (Massana/Pal) | text |

Possible snow sensor values: `ok` · `groga` · `taronja` · `vermella` · `negra`

**Binary Sensors**

| Entity ID | ON when... |
|-----------|-----------|
| `binary_sensor.andorra_mobilitat_talls_de_circulacio_actius` | Any road is closed |
| `binary_sensor.andorra_mobilitat_color_neu_actiu_qualsevol_carretera` | Any CG in active phase |
| `binary_sensor.andorra_mobilitat_prealerta_taronja_vermella_negra` | CG in orange / red / black phase |

### 🤖 Automation example

**Notification when CG-2 reaches red or black phase**
```yaml
automation:
  - alias: "Alert CG-2 Envalira severe phase"
    trigger:
      - platform: state
        entity_id: sensor.andorra_mobilitat_color_neu_cg2
        to: ["vermella", "negra"]
    action:
      - service: notify.mobile_app_my_phone
        data:
          title: "⛔ CG-2 Envalira"
          message: >
            Phase {{ states('sensor.andorra_mobilitat_color_neu_cg2') | upper }}
            activated. Check road conditions before leaving.
```

</details>

<details>
<summary>🇵🇹 Português</summary>

## Andorra Mobilitat — Componente personalizado para Home Assistant

Integração não oficial que lê em tempo real os dados de **mobilitat.ad** (Govern d'Andorra).
Não é necessária nenhuma chave de API nem registo.

### ⚡ Instalação rápida

**Opção A — Manual**
1. Copie a pasta `custom_components/andorra_mobilitat/` para a pasta `custom_components/` do seu HA.
2. Reinicie o HA.
3. Vá a **Configuração → Integrações → + Adicionar integração** e pesquise **Andorra Mobilitat**.
4. Introduza o intervalo de atualização (5 minutos por padrão) e confirme.
<img src="brands/icon@2x.png" width="100"/>

**Opção B — HACS**
Adicione o repositório como custom repository no HACS e instale a partir daí.

### 🌡️ Entidades criadas

**Sensores**

| Entity ID | Descrição | Unidade |
|-----------|-----------|---------|
| `sensor.andorra_mobilitat_incidencies_andorra` | Total de incidentes ativos | incidències |
| `sensor.andorra_mobilitat_talls_de_circulacio` | Número de cortes ativos | talls |
| `sensor.andorra_mobilitat_obres_en_carretera` | Número de obras ativas | obres |
| `sensor.andorra_mobilitat_fase_neu_pitjor_activa` | Fase de neve mais grave agora | texto |
| `sensor.andorra_mobilitat_color_neu_cg1` | Cor neve CG-1 (Andorra-Espanha) | texto |
| `sensor.andorra_mobilitat_color_neu_cg2` | Cor neve CG-2 (Envalira/Pas) | texto |
| `sensor.andorra_mobilitat_color_neu_cg3` | Cor neve CG-3 (Ordino/Serrat) | texto |
| `sensor.andorra_mobilitat_color_neu_cg4` | Cor neve CG-4 (Massana/Pal) | texto |

Valores possíveis dos sensores de neve: `ok` · `groga` · `taronja` · `vermella` · `negra`

**Sensores binários**

| Entity ID | ON quando... |
|-----------|-------------|
| `binary_sensor.andorra_mobilitat_talls_de_circulacio_actius` | Alguma estrada cortada |
| `binary_sensor.andorra_mobilitat_color_neu_actiu_qualsevol_carretera` | Qualquer CG em fase ativa |
| `binary_sensor.andorra_mobilitat_prealerta_taronja_vermella_negra` | CG em fase laranja / vermelha / negra |

### 🤖 Exemplo de automatização

**Notificação quando CG-2 passa para fase vermelha ou negra**
```yaml
automation:
  - alias: "Alerta CG-2 Envalira fase grave"
    trigger:
      - platform: state
        entity_id: sensor.andorra_mobilitat_color_neu_cg2
        to: ["vermella", "negra"]
    action:
      - service: notify.mobile_app_o_meu_telefone
        data:
          title: "⛔ CG-2 Envalira"
          message: >
            Fase {{ states('sensor.andorra_mobilitat_color_neu_cg2') | upper }}
            ativada. Verifique as condições antes de sair.
```

</details>

---

## Instal·lació ràpida

### Opció A — Manual
1. Copia la carpeta `custom_components/andorra_mobilitat/` a la carpeta `custom_components/` del teu HA.
2. Reinicia HA.
3. Ves a **Configuració → Integracions → + Afegir integració** i cerca **Andorra Mobilitat**.
4. Introdueix l'interval d'actualització (per defecte 5 minuts) i accepta.
<img src="brands/icon@2x.png" width="100"/>

### Opció B — HACS
Afegeix el repositori com a custom repository a HACS i instal·la des d'allà.

---

## 🌡️ Entitats creades

### Sensors

| Entity ID | Descripció | Unitat |
|-----------|-----------|--------|
| `sensor.andorra_mobilitat_incidencies_andorra` | Total incidències actives | incidències |
| `sensor.andorra_mobilitat_talls_de_circulacio` | Nombre de talls actius | talls |
| `sensor.andorra_mobilitat_obres_en_carretera` | Nombre d'obres actives | obres |
| `sensor.andorra_mobilitat_fase_neu_pitjor_activa` | Fase de neu més greu ara | text |
| `sensor.andorra_mobilitat_color_neu_cg1` | Color de neu CG-1 (Andorra-Espanya) | text |
| `sensor.andorra_mobilitat_color_neu_cg2` | Color de neu CG-2 (Envalira/Pas) | text |
| `sensor.andorra_mobilitat_color_neu_cg3` | Color de neu CG-3 (Ordino/Serrat) | text |
| `sensor.andorra_mobilitat_color_neu_cg4` | Color de neu CG-4 (Massana/Pal) | text |

**Valors possibles dels sensors de neu:** `ok` · `groga` · `taronja` · `vermella` · `negra`

### Binary Sensors

| Entity ID | ON quan... |
|-----------|-----------|
| `binary_sensor.andorra_mobilitat_talls_de_circulacio_actius` | Hi ha carreteres tallades |
| `binary_sensor.andorra_mobilitat_color_neu_actiu_qualsevol_carretera` | Qualsevol CG en fase activa |
| `binary_sensor.andorra_mobilitat_prealerta_taronja_vermella_negra` | CG en fase taronja / vermella / negra |

---

## 🤖 Exemples d'automatitzacions

### Notificació quan CG-2 passa a fase vermella o negra
```yaml
automation:
  - alias: "Alerta CG-2 Envalira fase greu"
    trigger:
      - platform: state
        entity_id: sensor.andorra_mobilitat_color_neu_cg2
        to:
          - "vermella"
          - "negra"
    action:
      - service: notify.mobile_app_el_meu_telefon
        data:
          title: "⛔ CG-2 Envalira"
          message: >
            Fase {{ states('sensor.andorra_mobilitat_color_neu_cg2') | upper }}
            activada. Comprova les condicions abans de sortir.
```

### Notificació de qualsevol tall nou
```yaml
automation:
  - alias: "Tall de circulació nou"
    trigger:
      - platform: state
        entity_id: binary_sensor.andorra_mobilitat_talls_de_circulacio_actius
        to: "on"
    action:
      - service: notify.mobile_app_el_meu_telefon
        data:
          title: "🚧 Tall de circulació Andorra"
          message: >
            Hi ha {{ states('sensor.andorra_mobilitat_talls_de_circulacio') }}
            tall(s) actiu(s).
            {% set talls = state_attr('sensor.andorra_mobilitat_talls_de_circulacio','llista') %}
            {% if talls %}{{ talls[0][:100] }}{% endif %}
```

### Mostrar a la matriu LED 64×64 el color de neu de CG-2
```yaml
automation:
  - alias: "Matriu LED — Color Neu CG-2"
    trigger:
      - platform: state
        entity_id: sensor.andorra_mobilitat_color_neu_cg2
    action:
      - service: shell_command.scroll_text_matrix
        data:
          text: >
            ❄ CG-2: {{ states('sensor.andorra_mobilitat_color_neu_cg2') | upper }}
```

---

## 🗂️ Estructura de fitxers

```
custom_components/
└── andorra_mobilitat/
    ├── __init__.py
    ├── manifest.json
    ├── const.py
    ├── coordinator.py
    ├── config_flow.py
    ├── sensor.py
    ├── binary_sensor.py
    ├── strings.json
    └── translations/
        ├── ca.json
        ├── es.json
        ├── en.json
        ├── fr.json
        ├── pt.json
        └── de.json
```

---

## ℹ️ Notes tècniques

- **Font de dades:** Scraping HTML de `https://www.mobilitat.ad/totes-incidencies`
- **Cap CORS** — el fetch es fa des del servidor HA, no des del navegador
- **Dependència:** `beautifulsoup4` (s'instal·la automàticament via `requirements` del manifest)
- **Rate:** Respectuós amb el servidor; interval mínim 1 minut, per defecte 5 minuts
- **Compatibilitat:** HA 2024.1+ (testejat a 2026.2)
