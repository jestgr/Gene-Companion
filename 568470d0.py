import streamlit as st
from datetime import date

st.set_page_config(page_title="GeoPro Camp Companion", layout="wide")

if "state" not in st.session_state:
    st.session_state.state = {
        "checklists": {
            "Travel": ["Hitch up trailer", "Check tire pressure", "Secure loose items"],
            "Camp Setup": ["Level trailer", "Connect power", "Connect water", "Set up sewer"],
            "Camp Tear Down": ["Disconnect utilities", "Stow awning", "Secure interior"],
            "Dumping": ["Gloves on", "Black tank first", "Flush hose", "Stow hose"],
            "Winterizing": ["Drain tanks", "Bypass water heater", "Add antifreeze", "Protect battery"],
            "Dewinterizing": ["Flush lines", "Sanitize system", "Check leaks", "Test appliances"],
        },
        "gear": [
            {"item": "Water hose", "location": "Pass-through bin", "category": "Water", "packed": False},
            {"item": "Sewer hose", "location": "Rear storage", "category": "Sewer", "packed": False},
            {"item": "Wheel chocks", "location": "Front bin", "category": "Safety", "packed": False},
        ],
        "campgrounds": [
            {"name": "", "status": "Want to visit", "hookups": "", "level": "", "notes": ""}
        ],
    }

state = st.session_state.state
st.title("GeoPro Camp Companion")
st.caption("A simple mobile-friendly RV app for checklists, gear, and campgrounds.")

tab1, tab2, tab3, tab4 = st.tabs(["Checklists", "Gear", "Campgrounds", "About"])

with tab1:
    st.subheader("Trip and maintenance checklists")
    checklist_names = list(state["checklists"].keys())
    selected = st.selectbox("Choose a checklist", checklist_names)
    items = state["checklists"][selected]

    cols = st.columns([3,1])
    with cols[0]:
        new_item = st.text_input("Add an item", key=f"new_{selected}")
    with cols[1]:
        if st.button("Add", key=f"add_{selected}") and new_item.strip():
            items.append(new_item.strip())
            st.rerun()

    for i, item in enumerate(items):
        c1, c2, c3 = st.columns([0.1, 0.75, 0.15])
        checked = c1.checkbox("", key=f"chk_{selected}_{i}")
        c2.markdown(f"<span style='color:gray;'>{item}</span>" if checked else item, unsafe_allow_html=True)
        if c3.button("Edit", key=f"edit_{selected}_{i}"):
            edited = st.text_input("Edit item", value=item, key=f"editbox_{selected}_{i}")
            if st.button("Save", key=f"save_{selected}_{i}") and edited.strip():
                items[i] = edited.strip()
                st.rerun()

    if st.button("Clear all checks", key=f"clear_{selected}"):
        for k in list(st.session_state.keys()):
            if k.startswith(f"chk_{selected}_"):
                st.session_state[k] = False
        st.rerun()

with tab2:
    st.subheader("Gear inventory")
    for idx, g in enumerate(state["gear"]):
        a,b,c,d = st.columns([0.35,0.25,0.25,0.15])
        g["item"] = a.text_input("Item", value=g["item"], key=f"gear_item_{idx}")
        g["location"] = b.text_input("Location", value=g["location"], key=f"gear_loc_{idx}")
        g["category"] = c.text_input("Category", value=g["category"], key=f"gear_cat_{idx}")
        g["packed"] = d.checkbox("Packed", value=g["packed"], key=f"gear_packed_{idx}")
    if st.button("Add gear item"):
        state["gear"].append({"item": "New item", "location": "", "category": "", "packed": False})
        st.rerun()

with tab3:
    st.subheader("Campground list")
    for idx, cg in enumerate(state["campgrounds"]):
        st.markdown(f"### Campground {idx+1}")
        cg["name"] = st.text_input("Name", value=cg["name"], key=f"cg_name_{idx}")
        cg["status"] = st.selectbox("Status", ["Want to visit", "Visited"], index=0 if cg["status"]=="Want to visit" else 1, key=f"cg_status_{idx}")
        cg["hookups"] = st.text_input("Hookups", value=cg["hookups"], key=f"cg_hookups_{idx}")
        cg["level"] = st.text_input("Level/site notes", value=cg["level"], key=f"cg_level_{idx}")
        cg["notes"] = st.text_area("Notes", value=cg["notes"], key=f"cg_notes_{idx}")
    if st.button("Add campground"):
        state["campgrounds"].append({"name": "", "status": "Want to visit", "hookups": "", "level": "", "notes": ""})
        st.rerun()

with tab4:
    st.write("This first version is an offline, editable RV organizer. Next steps could include save/load, cloud sync, campground import, reminders, and photo support.")
