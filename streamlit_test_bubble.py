import pyvista as pv
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import tempfile



def get_allegiance_styles():
    groups = [
        'Independent', 'Alliance', 'Empire', 'Federation', 'Guardian',
        'Thargoid', 'Pilots Federation', 'Player Pilots', 'No_Allegiance'
    ]

  
    base_styles = {
        "Federation": {"color": "red", "opacity": 0.6, "psize": 4, "metallic": 0.1, "specular": 0.7, "specular_power": 50, 'ambient': 0.2, 'diffuse': 0.8, 'emissive': 0.6,'pstyle':'points'},
        "Independent": {"color": "yellow", "opacity": 0.5, "psize": 3, "metallic": 0.1, "specular": 0.3, "specular_power": 50, 'ambient': 0.2, 'diffuse': 0.8, 'emissive': 0.6,'pstyle':'points'},
        "Empire": {"color": "blue", "opacity": 0.8, "psize": 4, "metallic": 0.5, "specular": 0.4, "specular_power": 128, 'ambient': 1.0, 'diffuse': 0.5, 'emissive': .6,'pstyle':'points'},
        "Alliance": {"color": "green", "opacity": 0.5, "psize": 3, "metallic": 0.5, "specular": 0.3, "specular_power": 128, 'ambient': 0.8, 'diffuse': 0.9, 'emissive': .4,'pstyle':'points'},
        "Pilots Federation": {"color": "magenta", "opacity": 0.3, "psize": 2, "metallic": 0.1, "specular": 0.0, "specular_power": 30, 'ambient': 0.2, 'diffuse': 0.2, 'emissive': 0.6,'pstyle':'points'},
        "Thargoid": {"color": (0.1, 0.9, 0.2), "opacity": 0.8, "psize": 4, "metallic": 0.8, "specular": 0.8, "specular_power": 100, 'ambient': 0.8, 'diffuse': 0.2, 'emissive': 1, 'pstyle':'points_gaussian'},
        "Guardian": {"color": '#7DF9FF', "opacity": 0.8, "psize": 4, "metallic": 0.8, "specular": 0.8, "specular_power": 100, 'ambient': 0.8, 'diffuse': 0.2, 'emissive': 1,'pstyle':'points_gaussian'},
        "Player Pilots": {"color": "grey", "opacity": 0.3, "psize": 2, "metallic": 0.1, "specular": 0.0, "specular_power": 30, 'ambient': 0.2, 'diffuse': 0.2, 'emissive': 0.1,'pstyle':'points'},
        "No_Allegiance": {"color": "black", "opacity": 0.01, "psize": 2, "metallic": 0.1, "specular": 0.0, "specular_power": 30, 'ambient': 0.2, 'diffuse': 0.2, 'emissive': 0.1,'pstyle':'points'}
    }

    gain_styles = {
        k: {**v, "opacity": max(v["opacity"], 0.6), "psize": max(v["psize"], 5)}
        for k, v in base_styles.items()
    }

    return groups, base_styles, gain_styles



#df = pd.read_csv('G:/Elite/Spansh_Data/2025/bubble/bubble_4500ly_time20250822_1.csv')
df = pd.read_csv('G:/Elite/Spansh_Data/2025/bubble/startbubble.csv')
points = df[['x','y','z']].to_numpy()
df[["y", "z"]] = df[["z", "y"]]  # Swap columns in-place

# Filter columns that include 'allegiance' in their names
allegiance_columns = [col for col in df.columns if 'allegiance' in col.lower()]
#population_columns = [col for col in df.columns if 'population' in col.lower()]

# go get the styles ready for plotting 
groups, allegiance_styles, allegiance_gain_styles = get_allegiance_styles()


#starting_allegiance_df0 =  df[['systemId64','x','y','z',allegiance_columns[0]]]
#starting_allegiance_df0 =starting_allegiance_df0.copy()   
#starting_allegiance_df0.rename(columns={allegiance_columns[0]:'allegiance'}, inplace=True)

#mask_current = starting_allegiance_df0['allegiance'] == 'No_Allegiance'
#starting_allegiance_df0=starting_allegiance_df0[~mask_current]

current_single_df = df.copy()

pl = pv.Plotter(off_screen=False)
#pl = pv.Plotter()
for group in groups:
                  
      pts = current_single_df[current_single_df['allegiance'] == group][['x', 'y', 'z']].to_numpy()
      pts = np.array(pts, dtype=np.float32)

      if pts.size == 0:
          continue
            
      cloud = pv.PolyData(pts)
      style = allegiance_styles.get(group, {"color": "grey", "opacity": 0.1, "psize": 1})
      pl.add_mesh(cloud, lighting=True,pbr=True,render_points_as_spheres=True,
                point_size=style["psize"], opacity=style["opacity"],
                color=style["color"], metallic =style["metallic"],specular=style["specular"] , specular_power=style["specular_power"] ,
                ambient=style["ambient"], diffuse=style["diffuse"] ,emissive=style["emissive"],name=f"static_{group}")
      


# Optional: set camera position and focal point
#plotter.camera_position = 'xy'  # or use a tuple of (position, focal_point, view_up)

# Export to HTML
st.title("Interactive 3D Point Cloud Viewer")

# Embed the PyVista scene

cam_x = st.slider("Camera X", -5000, 5000, 0)
cam_y = st.slider("Camera Y", -5000, 5000, 0)
cam_z = st.slider("Camera Z", -5000, 5000, 1000)

focal_x = st.slider("Focal X", -5000, 5000, 0)
focal_y = st.slider("Focal Y", -5000, 5000, 0)
focal_z = st.slider("Focal Z", -5000, 5000, 0)

pl.camera_position = [(cam_x, cam_y, cam_z), (focal_x, focal_y, focal_z), (0, 0, 1)]

with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
    pl.export_html(tmpfile.name)
    tmpfile.seek(0)
    html_str = tmpfile.read().decode("utf-8")

components.html(html_str, height=600)



#pl.show()