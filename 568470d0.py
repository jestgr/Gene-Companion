import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="GeoPro Camp Companion", page_icon="🏕️", layout="centered")
DATA_FILE = Path('output/geopro_data.json')
DEFAULT_VERSION = "1.0 portrait adaptive fixed"

DEFAULT_DATA = {
    "version": DEFAULT_VERSION,
    "checklists": {
        "Travel": [
            {"text": "Hitch up trailer", "done": False},
            {"text": "Check tire pressure", "done": False},
            {"text": "Secure loose items", "done": False},
        ],
        "Camp Setup": [
            {"text": "Level trailer", "done": False},
            {"text": "Connect power", "done": False},
            {"text": "Connect water", "done": False},
            {"text": "Connect sewer", "done": False},
        ],
        "Camp Tear Down": [
            {"text": "Disconnect utilities", "done": False},
            {"text": "Stow awning", "done": False},
            {"text": "Secure interior", "done": False},
        ],
        "Dumping": [
            {"text": "Gloves on", "done": False},
            {"text": "Black tank first", "done": False},
            {"text": "Flush hose", "done": False},
            {"text": "Stow hose", "done": False},
        ],
        "Winterizing": [
            {"text": "Drain fresh tank", "done": False},
            {"text": "Bypass water heater", "done": False},
            {"text": "Add antifreeze", "done": False},
            {"text": "Protect battery", "done": False},
        ],
        "Dewinterizing": [
            {"text": "Flush lines", "done": False},
            {"text": "Sanitize system", "done": False},
            {"text": "Check leaks", "done": False},
            {"text": "Test appliances", "done": False},
        ],
    },
    "gear": [
        {"item": "Water hose", "location": "Pass-through bin", "category": "Water", "packed": False, "open": False},
        {"item": "Sewer hose", "location": "Rear storage", "category": "Sewer", "packed": False, "open": False},
        {"item": "Wheel chocks", "location": "Front bin", "category": "Safety", "packed": False, "open": False},
    ],
    "campgrounds": [
        {"name": "", "status": "Want to visit", "hookups": "", "level": "", "notes": ""}
    ],
}

SAGE = "#A8D5BA"
CANTALOUPE = "#E8B4A3"
BORDER = "rgba(31,41,55,0.12)"
TEXT = "#1F2937"
CARD_BG = "rgba(255,255,255,0.86)"
MUTED = "#6B7280"


def deep_copy(obj):
    return json.loads(json.dumps(obj))


def load_data():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text())
            if not isinstance(data, dict):
                return deep_copy(DEFAULT_DATA)
            data.setdefault("version", DEFAULT_VERSION)
            data.setdefault("checklists", deep_copy(DEFAULT_DATA["checklists"]))
            data.setdefault("gear", deep_copy(DEFAULT_DATA["gear"]))
            data.setdefault("campgrounds", deep_copy(DEFAULT_DATA["campgrounds"]))
            return data
        except Exception:
            pass
    return deep_copy(DEFAULT_DATA)


def save_data():
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(st.session_state.data, indent=2))


if "data" not in st.session_state:
    st.session_state.data = load_data()
if "edit_open" not in st.session_state:
    st.session_state.edit_open = {}

data = st.session_state.data

checklists = data.get("checklists")
if not isinstance(checklists, dict):
    checklists = deep_copy(DEFAULT_DATA["checklists"])
    data["checklists"] = checklists

gear_list = data.get("gear")
if not isinstance(gear_list, list):
    gear_list = deep_copy(DEFAULT_DATA["gear"])
    data["gear"] = gear_list

campgrounds = data.get("campgrounds")
if not isinstance(campgrounds, list):
    campgrounds = deep_copy(DEFAULT_DATA["campgrounds"])
    data["campgrounds"] = campgrounds

st.markdown(f"""
<style>
:root {{
  --sage: {SAGE};
  --cantaloupe: {CANTALOUPE};
  --border: {BORDER};
  --text: {TEXT};
  --card: {CARD_BG};
  --muted: {MUTED};
}}
html, body, [class*='css'] {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
.stApp {{ background: linear-gradient(180deg, rgba(168,213,186,0.10), rgba(255,255,255,0.0)); color: var(--text); }}
.stButton > button {{ border-radius: 999px !important; border: 1px solid var(--border) !important; background: white !important; padding: 0.20rem 0.45rem !important; min-height: 1.85rem !important; font-size: 0.78rem !important; line-height: 1 !important; }}
.stButton > button:hover {{ border-color: var(--sage) !important; background: rgba(168,213,186,0.10) !important; }}
button[kind='primary'] {{ background: var(--sage) !important; color: #102016 !important; border: none !important; }}
button[kind='primary']:hover {{ background: var(--cantaloupe) !important; }}
.rowcard {{ border: 1px solid var(--border); border-radius: 16px; padding: 0.24rem 0.28rem; margin-bottom: 0.22rem; background: var(--card); box-shadow: 0 1px 8px rgba(0,0,0,0.03); }}
.itemtext {{ font-size: 0.88rem; line-height: 1.0; word-break: break-word; margin: 0; padding: 0; }}
.itemdone {{ color: #9CA3AF; }}
.gearpanel {{ margin-top: 0.18rem; padding: 0.24rem; border-radius: 12px; border: 1px solid rgba(168,213,186,0.35); background: rgba(168,213,186,0.08); }}
.smalllabel {{ color: var(--muted); font-size: 0.68rem; margin-bottom: 0.03rem; }}
@media (max-width: 480px) {{
  .itemtext {{ font-size: 0.82rem; }}
  .stButton > button {{ font-size: 0.72rem !important; padding: 0.16rem 0.34rem !important; min-height: 1.65rem !important; }}
  .rowcard {{ padding: 0.18rem 0.22rem; margin-bottom: 0.18rem; }}
}}
</style>
""", unsafe_allow_html=True)

st.title("🏕️ GeoPro Camp Companion")
st.caption(f"Version {data.get('version', DEFAULT_VERSION)} • autosaves locally")
menu = st.radio("Go to", ["Checklists", "Gear", "Campgrounds", "About"], horizontal=True, label_visibility="collapsed")

if menu == "Checklists":
    st.subheader("Checklists")
    selected = st.selectbox("List", list(checklists.keys()), label_visibility="collapsed")
    items = checklists[selected]
    new_item = st.text_input("Add item", placeholder="Add new checklist item")
    if st.button("Add item", type="primary") and new_item.strip():
        items.append({"text": new_item.strip(), "done": False})
        save_data()
        st.rerun()

    for i, item in enumerate(items):
        c1, c2, c3 = st.columns([0.08, 0.78, 0.14], vertical_alignment="center")
        done = c1.checkbox("", value=item.get("done", False), key=f"chk_{selected}_{i}", label_visibility="collapsed")
        item["done"] = done
        c2.markdown(f"<div class='itemtext {'itemdone' if done else ''}'>{item['text']}</div>", unsafe_allow_html=True)
        if c3.button("E", key=f"edit_{selected}_{i}"):
            st.session_state.edit_open[f"{selected}_{i}"] = not st.session_state.edit_open.get(f"{selected}_{i}", False)

        if st.session_state.edit_open.get(f"{selected}_{i}"):
            e1, e2 = st.columns([0.85, 0.15], vertical_alignment="center")
            edited = e1.text_input("", value=item["text"], key=f"editbox_{selected}_{i}", label_visibility="collapsed")
            if e2.button("X", key=f"del_{selected}_{i}"):
                items.pop(i)
                st.session_state.edit_open.pop(f"{selected}_{i}", None)
                save_data()
                st.rerun()
            if st.button("Save", key=f"save_{selected}_{i}") and edited.strip():
                item["text"] = edited.strip()
                st.session_state.edit_open.pop(f"{selected}_{i}", None)
                save_data()
                st.rerun()

    a, b = st.columns(2)
    if a.button("Clear checks"):
        for item in items:
            item["done"] = False
        for k in list(st.session_state.keys()):
            if k.startswith(f"chk_{selected}_"):
                st.session_state[k] = False
        save_data()
        st.rerun()
    if b.button("Reset list"):
        checklists[selected] = deep_copy(DEFAULT_DATA["checklists"][selected])
        save_data()
        st.rerun()

elif menu == "Gear":
    st.subheader("Gear")
    if st.button("Add gear item", type="primary"):
        gear_list.append({"item": "New item", "location": "", "category": "", "packed": False, "open": False})
        save_data()
        st.rerun()

    for i, g in enumerate(gear_list):
        if not isinstance(g, dict):
            gear_list[i] = {"item": str(g), "location": "", "category": "", "packed": False, "open": False}
            g = gear_list[i]
        g.setdefault("item", "")
        g.setdefault("location", "")
        g.setdefault("category", "")
        g.setdefault("packed", False)
        g.setdefault("open", False)

        c1, c2, c3 = st.columns([0.08, 0.78, 0.14], vertical_alignment="center")
        g["packed"] = c1.checkbox("", value=bool(g.get("packed", False)), key=f"gear_packed_{i}", label_visibility="collapsed")
        if c2.button(str(g.get("item", "")), key=f"gear_toggle_{i}"):
            g["open"] = not bool(g.get("open", False))
            save_data()
            st.rerun()
        if c3.button("X", key=f"gear_del_{i}"):
            gear_list.pop(i)
            save_data()
            st.rerun()

        if g.get("open", False):
            c1a, c2a = st.columns(2)
            c1a.markdown("<div class='smalllabel'>Category</div>", unsafe_allow_html=True)
            g["category"] = c1a.text_input("", value=str(g.get("category", "")), key=f"gear_cat_{i}", label_visibility="collapsed")
            c2a.markdown("<div class='smalllabel'>Location</div>", unsafe_allow_html=True)
            g["location"] = c2a.text_input("", value=str(g.get("location", "")), key=f"gear_loc_{i}", label_visibility="collapsed")

    if st.button("Collapse all gear"):
        for g in gear_list:
            if isinstance(g, dict):
                g["open"] = False
        save_data()
        st.rerun()

elif menu == "Campgrounds":
    st.subheader("Campgrounds")
    if st.button("Add campground", type="primary"):
        campgrounds.append({"name": "", "status": "Want to visit", "hookups": "", "level": "", "notes": ""})
        save_data()
        st.rerun()
    for i, cg in enumerate(campgrounds):
        if not isinstance(cg, dict):
            campgrounds[i] = {"name": str(cg), "status": "Want to visit", "hookups": "", "level": "", "notes": ""}
            cg = campgrounds[i]
        with st.container(border=True):
            cg["name"] = st.text_input("Name", value=str(cg.get("name", "")), key=f"c_name_{i}")
            cg["status"] = st.radio("Status", ["Want to visit", "Visited"], index=0 if cg.get("status", "Want to visit") == "Want to visit" else 1, horizontal=True, key=f"c_status_{i}")
            x, y = st.columns(2)
            cg["hookups"] = x.text_input("Hookups", value=str(cg.get("hookups", "")), key=f"c_hookups_{i}")
            cg["level"] = y.text_input("Level", value=str(cg.get("level", "")), key=f"c_level_{i}")
            cg["notes"] = st.text_area("Notes", value=str(cg.get("notes", "")), key=f"c_notes_{i}")
            if st.button("Remove campground", key=f"c_del_{i}"):
                campgrounds.pop(i)
                save_data()
                st.rerun()

else:
    st.subheader("About")
    st.write("Minimalist, compact, and persistent. Checklist rows are one line; gear expands inline on tap.")
    st.write("Data saves to output/geopro_data.json in the app environment.")
    if st.button("Force save now"):
        save_data()
        st.success("Saved.")
