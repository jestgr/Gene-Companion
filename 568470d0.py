import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="GeoPro Camp Companion", page_icon="🏕️", layout="centered")
DATA_FILE = Path('output/geopro_data.json')
DEFAULT_VERSION = "0.6 polished compact"

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
    "campgrounds": [{"name": "", "status": "Want to visit", "hookups": "", "level": "", "notes": ""}],
}

SAGE = "#A8D5BA"
CANTALOUPE = "#E8B4A3"
BORDER = "rgba(31,41,55,0.12)"
TEXT = "#1F2937"
MUTED = "#6B7280"
CARD_BG = "rgba(255,255,255,0.86)"


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


if "data" not in st.session_state:
    st.session_state.data = load_data()
if "edit_open" not in st.session_state:
    st.session_state.edit_open = {}

data = st.session_state.data

st.markdown(f"""
<style>
:root {{
  --sage: {SAGE};
  --cantaloupe: {CANTALOUPE};
  --border: {BORDER};
  --text: {TEXT};
  --muted: {MUTED};
  --card: {CARD_BG};
}}
html, body, [class*='css'] {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}}
.stApp {{
  background: linear-gradient(180deg, rgba(168,213,186,0.10), rgba(255,255,255,0.0));
  color: var(--text);
}}
.stButton > button {
    padding: 0.20rem 0.45rem !important;
    min-height: 1.9rem !important;
    font-size: 0.82rem !important;
    border-radius: 999px !important;
}
.rowcard {
    padding: 0.35rem 0.45rem !important;
    margin-bottom: 0.30rem !important;
}
.itemtext {
    font-size: 0.95rem !important;
    line-height: 1.05 !important;
}
.gearpanel {
    margin-top: 0.30rem !important;
    padding: 0.40rem !important;
}
.smalllabel {
    font-size: 0.74rem !important;
    margin-bottom: 0.08rem !important;
}
.stButton > button {{
  border-radius: 999px;
  border: 1px solid var(--border);
  background: white;
  padding: 0.32rem 0.72rem;
  font-size: 0.93rem;
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
.rowcard {{
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 0.55rem 0.65rem;
  margin-bottom: 0.45rem;
  background: var(--card);
  box-shadow: 0 1px 8px rgba(0,0,0,0.03);
}}
.itemtext {{
  font-size: 1rem;
  line-height: 1.2;
  flex: 1;
  word-break: break-word;
}}
.itemdone {{
  color: #9CA3AF;
  text-decoration: none;
}}
.gearpanel {{
  margin-top: 0.5rem;
  padding: 0.55rem;
  border-radius: 16px;
  border: 1px solid rgba(168,213,186,0.35);
  background: rgba(168,213,186,0.08);
}}
.smalllabel {{
  color: var(--muted);
  font-size: 0.82rem;
  margin-bottom: 0.15rem;
}}
.pill {{
  display: inline-block;
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
  background: rgba(232,180,163,0.16);
  color: #6b4e45;
  font-size: 0.8rem;
}}
</style>
""", unsafe_allow_html=True)

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
    row = st.columns([0.08, 0.78, 0.14], vertical_alignment="center")
    done = row[0].checkbox("", value=item.get("done", False), key=f"chk_{selected}_{i}", label_visibility="collapsed")
    item["done"] = done
    row[1].markdown(f"<div class='itemtext {'itemdone' if done else ''}'>{item['text']}</div>", unsafe_allow_html=True)
    if row[2].button("E", key=f"edit_{selected}_{i}"):
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
        st.markdown("</div>", unsafe_allow_html=True)

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
    row = st.columns([0.08, 0.78, 0.14], vertical_alignment="center")
    g["packed"] = row[0].checkbox("", value=g.get("packed", False), key=f"gear_packed_{i}", label_visibility="collapsed")
    if row[1].button(g.get("item", ""), key=f"gear_toggle_{i}"):
        g["open"] = not g.get("open", False)
        save_data()
        st.rerun()
    if row[2].button("X", key=f"gear_del_{i}"):
        data["gear"].pop(i)
        save_data()
        st.rerun()

    if g.get("open", False):
        with st.container():
            st.markdown("<div class='gearpanel'>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.markdown("<div class='smalllabel'>Category</div>", unsafe_allow_html=True)
            g["category"] = c1.text_input("", value=g.get("category", ""), key=f"gear_cat_{i}", label_visibility="collapsed")
            c2.markdown("<div class='smalllabel'>Location</div>", unsafe_allow_html=True)
            g["location"] = c2.text_input("", value=g.get("location", ""), key=f"gear_loc_{i}", label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True))

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
            x, y = st.columns(2)
            cg["hookups"] = x.text_input("Hookups", value=cg.get("hookups", ""), key=f"c_hookups_{i}")
            cg["level"] = y.text_input("Level", value=cg.get("level", ""), key=f"c_level_{i}")
            cg["notes"] = st.text_area("Notes", value=cg.get("notes", ""), key=f"c_notes_{i}")
            if st.button("Remove campground", key=f"c_del_{i}"):
                data["campgrounds"].pop(i)
                save_data()
                st.rerun()

else:
    st.subheader("About")
    st.write("Minimalist, compact, and persistent. Checklist rows are one line; gear expands inline on tap.")
    st.write("Data saves to output/geopro_data.json in the app environment.")
    if st.button("Force save now"):
        save_data()
        st.success("Saved.")
