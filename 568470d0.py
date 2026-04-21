import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="GeoPro Camp Companion", page_icon="🏕️", layout="centered")
DATA_FILE = Path('output/geopro_data.json')
DEFAULT_VERSION = "0.4 minimalist compact persistent"

DEFAULT_DATA = {
    "version": DEFAULT_VERSION,
    "checklists": {
        "Travel": [{"text": "Hitch up trailer", "done": False}, {"text": "Check tire pressure", "done": False}, {"text": "Secure loose items", "done": False}],
        "Camp Setup": [{"text": "Level trailer", "done": False}, {"text": "Connect power", "done": False}, {"text": "Connect water", "done": False}, {"text": "Connect sewer", "done": False}],
        "Camp Tear Down": [{"text": "Disconnect utilities", "done": False}, {"text": "Stow awning", "done": False}, {"text": "Secure interior", "done": False}],
        "Dumping": [{"text": "Gloves on", "done": False}, {"text": "Black tank first", "done": False}, {"text": "Flush hose", "done": False}, {"text": "Stow hose", "done": False}],
        "Winterizing": [{"text": "Drain fresh tank", "done": False}, {"text": "Bypass water heater", "done": False}, {"text": "Add antifreeze", "done": False}, {"text": "Protect battery", "done": False}],
        "Dewinterizing": [{"text": "Flush lines", "done": False}, {"text": "Sanitize system", "done": False}, {"text": "Check leaks", "done": False}, {"text": "Test appliances", "done": False}],
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
BORDER = "rgba(31,41,55,0.10)"
TEXT = "#1F2937"
MUTED = "#6B7280"


def deep_copy(obj):
    return json.loads(json.dumps(obj))


def load_data():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text())
            if "version" not in data:
                data["version"] = DEFAULT_VERSION
            return data
        except Exception:
            pass
    return deep_copy(DEFAULT_DATA)


def save_data():
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(st.session_state.data, indent=2))


def reset_defaults():
    st.session_state.data = deep_copy(DEFAULT_DATA)
    save_data()


if "data" not in st.session_state:
    st.session_state.data = load_data()
if "edit_open" not in st.session_state:
    st.session_state.edit_open = {}
if "theme" not in st.session_state:
    st.session_state.theme = "Light"


data = st.session_state.data

THEME_CSS = f"""
<style>
:root {{
  --sage: {SAGE};
  --cantaloupe: {CANTALOUPE};
  --border: {BORDER};
  --text: {TEXT};
  --muted: {MUTED};
}}
html, body, [class*='css'] {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}}
.stApp {{
  background: linear-gradient(180deg, rgba(168,213,186,0.12), rgba(255,255,255,0.0));
  color: var(--text);
}}
[data-testid='stRadio'] label, [data-testid='stSelectbox'] label, [data-testid='stTextInput'] label, [data-testid='stTextArea'] label {{
  font-size: 0.9rem;
}}
.stButton > button {{
  border-radius: 999px;
  border: 1px solid var(--border);
  background: white;
  padding: 0.4rem 0.8rem;
  font-size: 0.95rem;
}}
.stButton > button:hover {{
  border-color: var(--sage);
  background: rgba(168,213,186,0.10);
}}
button[kind='primary'] {{
  background: var(--sage) !important;
  color: #102016 !important;
  border: none !important;
}}
button[kind='primary']:hover {{
  background: var(--cantaloupe) !important;
}}
[data-testid='stCheckbox'] label {{
  gap: 0.25rem;
}}
.compact-item {{
  font-size: 1rem;
  line-height: 1.25;
}}
.small-muted {{
  color: var(--muted);
  font-size: 0.88rem;
}}
.card {{
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 0.7rem 0.75rem;
  margin-bottom: 0.5rem;
  background: rgba(255,255,255,0.78);
  box-shadow: 0 1px 8px rgba(0,0,0,0.03);
}}
.tight button {{
  padding: 0.2rem 0.5rem !important;
  font-size: 0.9rem !important;
  min-height: 2rem !important;
  border-radius: 999px !important;
}}
hr {{
  margin: 0.5rem 0;
}}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)
st.title("🏕️ GeoPro Camp Companion")
st.caption(f"Version {data.get('version', DEFAULT_VERSION)} • autosaves locally")

menu = st.radio("Go to", ["Checklists", "Gear", "Campgrounds", "About"], horizontal=True, label_visibility="collapsed")

if menu == "Checklists":
    st.subheader("Checklists")
    selected = st.selectbox("List", list(data["checklists"].keys()), label_visibility="collapsed")
    items = data["checklists"][selected]

    new_item = st.text_input("Add item", placeholder="Add new checklist item")
    if st.button("Add item", type="primary") and new_item.strip():
        items.append({"text": new_item.strip(), "done": False})
        save_data()
        st.rerun()

    for i, item in enumerate(items):
        with st.container(border=True):
            cols = st.columns([0.12, 0.70, 0.18], vertical_alignment="center")
            done = cols[0].checkbox("", value=item.get("done", False), key=f"chk_{selected}_{i}", label_visibility="collapsed")
            item["done"] = done
            cols[1].markdown(f"<div class='compact-item' style='color:#9CA3AF;'>{item['text']}</div>" if done else f"<div class='compact-item'>{item['text']}</div>", unsafe_allow_html=True)
            if cols[2].button("Edit", key=f"edit_{selected}_{i}"):
                st.session_state.edit_open[f"{selected}_{i}"] = not st.session_state.edit_open.get(f"{selected}_{i}", False)

            if st.session_state.edit_open.get(f"{selected}_{i}"):
                edit_cols = st.columns([0.72, 0.14, 0.14], vertical_alignment="center")
                edited = edit_cols[0].text_input("", value=item["text"], key=f"editbox_{selected}_{i}", label_visibility="collapsed")
                if edit_cols[1].button("Save", key=f"save_{selected}_{i}") and edited.strip():
                    item["text"] = edited.strip()
                    st.session_state.edit_open.pop(f"{selected}_{i}", None)
                    save_data()
                    st.rerun()
                if edit_cols[2].button("Del", key=f"del_{selected}_{i}"):
                    items.pop(i)
                    st.session_state.edit_open.pop(f"{selected}_{i}", None)
                    save_data()
                    st.rerun()

    c1, c2 = st.columns(2)
    if c1.button("Clear checks"):
        for item in items:
            item["done"] = False
        for k in list(st.session_state.keys()):
            if k.startswith(f"chk_{selected}_"):
                st.session_state[k] = False
        save_data()
        st.rerun()
    if c2.button("Reset list"):
        st.session_state.data["checklists"][selected] = deep_copy(DEFAULT_DATA["checklists"][selected])
        save_data()
        st.rerun()

elif menu == "Gear":
    st.subheader("Gear")
    if st.button("Add gear item", type="primary"):
        data["gear"].append({"item": "New item", "location": "", "category": "", "packed": False, "open": False})
        save_data()
        st.rerun()

    for i, g in enumerate(data["gear"]):
        with st.container(border=True):
            top = st.columns([0.12, 0.70, 0.18], vertical_alignment="center")
            g["packed"] = top[0].checkbox("", value=g.get("packed", False), key=f"gear_packed_{i}", label_visibility="collapsed")
            if top[1].button(g.get("item", ""), key=f"gear_toggle_{i}"):
                g["open"] = not g.get("open", False)
                save_data()
                st.rerun()
            if top[2].button("Del", key=f"gear_del_{i}"):
                data["gear"].pop(i)
                save_data()
                st.rerun()

            if g.get("open", False):
                left, right = st.columns(2, vertical_alignment="center")
                g["category"] = left.text_input("Category", value=g.get("category", ""), key=f"gear_cat_{i}")
                g["location"] = right.text_input("Location", value=g.get("location", ""), key=f"gear_loc_{i}")

    if st.button("Collapse all gear"):
        for g in data["gear"]:
            g["open"] = False
        save_data()
        st.rerun()

elif menu == "Campgrounds":
    st.subheader("Campgrounds")
    if st.button("Add campground", type="primary"):
        data["campgrounds"].append({"name": "", "status": "Want to visit", "hookups": "", "level": "", "notes": ""})
        save_data()
        st.rerun()
    for i, cg in enumerate(data["campgrounds"]):
        with st.container(border=True):
            cg["name"] = st.text_input("Name", value=cg.get("name", ""), key=f"c_name_{i}")
            cg["status"] = st.radio("Status", ["Want to visit", "Visited"], index=0 if cg.get("status", "Want to visit") == "Want to visit" else 1, horizontal=True, key=f"c_status_{i}")
            a, b = st.columns(2)
            cg["hookups"] = a.text_input("Hookups", value=cg.get("hookups", ""), key=f"c_hookups_{i}")
            cg["level"] = b.text_input("Level", value=cg.get("level", ""), key=f"c_level_{i}")
            cg["notes"] = st.text_area("Notes", value=cg.get("notes", ""), key=f"c_notes_{i}")
            if st.button("Remove campground", key=f"c_del_{i}"):
                data["campgrounds"].pop(i)
                save_data()
                st.rerun()

else:
    st.subheader("About")
    st.write("This build is minimalist, compact, and persistent. It uses calm sage and cantaloupe accents, with rounded controls and tap-to-expand details.")
    st.write("Data saves to output/geopro_data.json in the app environment.")
    if st.button("Force save now"):
        save_data()
        st.success("Saved.")
