import streamlit as st
import folium
from streamlit_folium import st_folium
import math
import random
import requests

# 地図の中心・初期現在地を明善寺と重ならないように正確な座標で設定
CENTER_LAT, CENTER_LON = 36.25543695113183, 136.90536905875567

spots = [
    {"name": "明善寺", "lat": 36.255883628077605, "lon": 136.90656264840985, "description": "白川郷を代表する合掌造りの寺院", "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/7e/Myouzenji_Shirakawa.JPG"},
    {"name": "白川八幡神社", "lat": 36.254918579759185, "lon": 136.90581872055262, "description": "毎年どぶろく祭りが行われる歴史ある神社", "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Shirakawa_Hachiman_Shrine_2017.jpg"},
    {"name": "荻町秋葉神社", "lat": 36.25674394600938, "lon": 136.90439427183114, "description": "火防の神を祀る小さな神社", "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Akiba_Shrine_Shirakawa-go_2012.jpg"},
    {"name": "白川鄉合掌村", "lat": 36.25632624675251, "lon": 136.9061610045663, "description": "合掌造り集落の中心的な観光エリア", "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80"},
    {"name": "和田家住宅", "lat": 36.26005184735733, "lon": 136.9077139323979, "description": "国指定重要文化財の合掌造り民家", "image_url": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Wada_house_Shirakawa-go_2012.jpg"},
    {"name": "荻町城跡展望台", "lat": 36.26332416485644, "lon": 136.90762818663734, "description": "集落全体を一望できる人気の展望スポット", "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Shirakawa-go_lookout_2012.jpg"},
    {"name": "神田家", "lat": 36.25812055792352, "lon": 136.90708365456294, "description": "江戸時代から続く合掌造りの民家", "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/6a/Kanda_house_Shirakawa-go_2012.jpg"},
]

congestion_levels = ["空いている", "やや混雑", "混雑"]
congestion_colors = {"空いている": "green", "やや混雑": "orange", "混雑": "red"}
congestion_icons = {"空いている": "🟢", "やや混雑": "🟠", "混雑": "🔴"}

# 混雑状況をセッションに保存し、ボタンでのみ更新
if "congestion" not in st.session_state or st.sidebar.button("混雑状況を更新", help="最新の混雑状況に更新します"):
    st.session_state.congestion = [random.choice(congestion_levels) for _ in spots]
for i, spot in enumerate(spots):
    spot["congestion"] = st.session_state.congestion[i]

# フィルター適用
filter_levels = []
if 'filter_empty' in st.session_state and st.session_state['filter_empty']: filter_levels.append("空いている")
if 'filter_some' in st.session_state and st.session_state['filter_some']: filter_levels.append("やや混雑")
if 'filter_busy' in st.session_state and st.session_state['filter_busy']: filter_levels.append("混雑")
filtered_spots = [s for s in spots if s["congestion"] in filter_levels] if filter_levels else spots
empty_spots = [s for s in filtered_spots if s["congestion"] == "空いている"]

# サイドバーUI改善
with st.sidebar:
    st.markdown("""
    <div style='background:#f7f7fa; border-radius:12px; border:1px solid #d0d0e0; padding:18px 18px 10px 18px; margin-bottom:18px;'>
        <span style='font-size:20px; font-weight:bold;'>現在地を入力</span><br>
        <span style='font-size:13px; color:#666;'>地図の中心や距離計算の基準になります</span>
        <div style='height:8px;'></div>
    """, unsafe_allow_html=True)
    user_lat = st.number_input("緯度", value=st.session_state.get("user_lat", CENTER_LAT), format="%.6f", key="lat_input")
    user_lon = st.number_input("経度", value=st.session_state.get("user_lon", CENTER_LON), format="%.6f", key="lon_input")
    if st.button("現在地を明善寺付近にリセット", key="reset_center"):
        st.session_state["lat_input"] = CENTER_LAT
        st.session_state["lon_input"] = CENTER_LON
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#f7f7fa; border-radius:12px; border:1px solid #d0d0e0; padding:18px 18px 10px 18px; margin-bottom:18px;'>
        <span style='font-size:20px; font-weight:bold;'>🧭 混雑度で絞り込み</span><br>
    """, unsafe_allow_html=True)
    filter_empty = st.checkbox("空いている", value=True, key="filter_empty")
    filter_some = st.checkbox("やや混雑", value=True, key="filter_some")
    filter_busy = st.checkbox("混雑", value=True, key="filter_busy")
    st.markdown("</div>", unsafe_allow_html=True)

    if empty_spots:
        st.markdown("""
        <div style='background:#e8fbe8; border-radius:12px; border:1px solid #b0e0b0; padding:16px 16px 8px 16px; margin-bottom:18px;'>
            <span style='font-size:18px; font-weight:bold; color:#228822;'>🟢 今空いているおすすめスポット</span><br>
        """, unsafe_allow_html=True)
        for s in empty_spots:
            st.markdown(f"<div style='margin-bottom:8px; padding-left:8px; font-size:16px;'>・{s['name']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#f0f4ff; border-radius:12px; border:1px solid #b0c4e0; padding:18px 18px 18px 18px; margin-bottom:18px; text-align:center;'>
        <span style='font-size:20px; font-weight:bold;'>🚶 おすすめルート自動作成</span><br>
        <span style='font-size:13px; color:#555;'>混雑度が低い順に観光地を自動選択し、ルートを自動表示します</span>
        <div style='margin:18px 0 10px 0;'></div>
        <div style='margin-bottom:10px; text-align:left;'>
            <input type='checkbox' id='avoid_congestion' name='avoid_congestion' style='zoom:1.2;' {% if st.session_state.get('avoid_congestion', False) %}checked{% endif %}>
            <label for='avoid_congestion' style='font-size:14px; color:#333; margin-left:6px;'>混雑を避けるルートを優先</label>
        </div>
    </div>
    """, unsafe_allow_html=True)
    avoid_congestion = st.checkbox("混雑を避けるルートを優先", value=st.session_state.get("avoid_congestion", False), key="avoid_congestion")
    if avoid_congestion:
        route_spots = [s for s in filtered_spots if s["congestion"] == "空いている"]
    else:
        route_spots = filtered_spots
    if st.button("おすすめルート自動作成（分散化）"):
        congestion_order = {"空いている": 0, "やや混雑": 1, "混雑": 2}
        sorted_names = [s["name"] for s in sorted(route_spots, key=lambda x: congestion_order[x["congestion"]])]
        st.session_state["selected_names"] = sorted_names
        st.session_state["show_route"] = True
        st.session_state["route_geojson"] = None
    if st.button("おすすめルートをもう一つ提案"):
        import random
        random_names = [s["name"] for s in route_spots]
        random.shuffle(random_names)
        st.session_state["selected_names"] = random_names
        st.session_state["show_route"] = True
        st.session_state["route_geojson"] = None

# サイドバーに「今空いているおすすめスポット」
if empty_spots:
    st.sidebar.markdown("""
    <div style='margin-top:24px; margin-bottom:8px; font-weight:bold; font-size:18px;'>
        🟢 今空いているおすすめスポット
    </div>
    """, unsafe_allow_html=True)
    for s in empty_spots:
        st.sidebar.markdown(f"<div style='margin-bottom:8px; padding-left:8px;'>・{s['name']}</div>", unsafe_allow_html=True)

# 距離計算
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2*R*math.asin(math.sqrt(a))

st.title("白川郷観光ルート・混雑マップ")

# 選択状態の管理
if "selected_names" not in st.session_state:
    st.session_state["selected_names"] = []
selected_names = st.multiselect(
    "訪れたい観光地を選択",
    [s["name"] for s in filtered_spots],
    default=[n for n in st.session_state["selected_names"] if n in [s["name"] for s in filtered_spots]]
)
st.session_state["selected_names"] = selected_names

# 選択スポットのみ抽出し、現在地からの距離を計算
selected_spots = [s.copy() for s in filtered_spots if s["name"] in selected_names]
for spot in selected_spots:
    spot["distance"] = haversine(user_lat, user_lon, spot["lat"], spot["lon"])

# 並び順切り替え
sort_mode = st.radio("表示順", ["距離順", "混雑順"], horizontal=True)
if sort_mode == "距離順":
    sorted_spots = sorted(selected_spots, key=lambda x: x["distance"])
else:
    congestion_order = {"混雑": 2, "やや混雑": 1, "空いている": 0}
    sorted_spots = sorted(selected_spots, key=lambda x: (congestion_order[x["congestion"]], x["distance"]))

# 地図の中心を現在地
m = folium.Map(location=[user_lat, user_lon], zoom_start=16)

# 現在地マーカー
folium.Marker(
    [user_lat, user_lon],
    icon=folium.Icon(color="blue", icon="user", prefix="fa"),
    popup="あなたの現在地"
).add_to(m)

# 混雑度ヒートマップ（CircleMarkerで大きさ・色の濃さを変える）
for spot in filtered_spots:
    if spot["congestion"] == "混雑":
        radius, color, opacity = 38, "red", 0.35
    elif spot["congestion"] == "やや混雑":
        radius, color, opacity = 28, "orange", 0.22
    else:
        radius, color, opacity = 18, "green", 0.12
    folium.Circle(
        location=[spot["lat"], spot["lon"]],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=opacity,
        weight=0,
    ).add_to(m)

# 選択スポットのみ地図上に色分け丸マーカー＋番号
for i, spot in enumerate(sorted_spots):
    color = congestion_colors[spot["congestion"]]
    gmap_url = f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"
    # 色枠＋番号マーカー
    icon_html = f"""
    <div style='display:flex; align-items:center; justify-content:center;'>
      <div style="
        width: 44px; height: 44px; border-radius: 50%;
        border: 6px solid {color};
        background: #fff;
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; font-weight: bold; color: #222; box-shadow: 0 0 8px #8884;
      ">{i+1}</div>
    </div>
    """
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        icon=folium.DivIcon(html=icon_html),
        popup=folium.Popup(f"""
        <div style='text-align:center;'>
          <img src='{spot.get('image_url','')}' width='220' style='border-radius:8px; margin-bottom:6px;'><br>
          <div style='font-size:18px; font-weight:bold; color:{color};'>
            {congestion_icons[spot['congestion']]} {spot['congestion']}
          </div>
          <div style='font-size:16px; margin-top:6px; font-weight:bold;'>
            {spot['name']}
          </div>
          <div style='font-size:14px; margin-top:4px; color:#333;'>
            {spot.get('description', '')}
          </div>
          <div style='margin-top:6px;'>
            <a href='{gmap_url}' target='_blank' style='font-size:13px; color:#1a73e8; text-decoration:underline;'>Googleマップで開く</a>
          </div>
        </div>
        """, max_width=260)
    ).add_to(m)

# ルート表示ボタン
if "show_route" not in st.session_state:
    st.session_state.show_route = False
if "route_geojson" not in st.session_state:
    st.session_state.route_geojson = None

if st.button("ルートを表示"):
    st.session_state.show_route = True
    st.session_state.route_geojson = None

# ルート表示フラグがTrueかつ1地点以上選択時のみAPIリクエスト
if st.session_state.show_route and len(sorted_spots) >= 1:
    if st.session_state.route_geojson is None:
        # 現在地を始点に追加
        coords = [[float(user_lon), float(user_lat)]]
        coords += [[float(spot["lon"]), float(spot["lat"])] for spot in sorted_spots]
        url = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"
        headers = {"Authorization": "5b3ce3597851110001cf6248d6db217408bb421ca0be5831d2694983", "Content-Type": "application/json"}
        body = {"coordinates": coords}
        try:
            response = requests.post(url, json=body, headers=headers, timeout=10)
            if response.status_code == 200:
                st.session_state.route_geojson = response.json()
            else:
                st.error(f"ルート取得に失敗しました: {response.status_code} {response.text}")
        except Exception as e:
            st.error(f"ルート取得時にエラー: {e}")
    if st.session_state.route_geojson:
        folium.GeoJson(st.session_state.route_geojson, name="route").add_to(m)

# 凡例（左下・小型パネル）
legend_html = '''
<div style="position: fixed; bottom: 24px; left: 24px; z-index:9999; background: rgba(255,255,255,0.92); border-radius: 10px; border: 1px solid #888; padding: 10px 16px; font-size: 14px; box-shadow: 2px 2px 6px #ccc; min-width:180px; max-width:260px;">
<b>混雑状況の凡例</b><br>
<div style="display: flex; gap: 10px; margin-top: 6px; align-items: flex-start; font-size:13px;">
  <span><span style="color:green; font-size:18px;">●</span> 空いています<br><span style='font-size:11px; color:#555;'>待ち時間ほぼなし</span></span>
  <span><span style="color:orange; font-size:18px;">●</span> やや混雑<br><span style='font-size:11px; color:#555;'>待ち時間10分程度</span></span>
  <span><span style="color:red; font-size:18px;">●</span> 混雑中<br><span style='font-size:11px; color:#555;'>待ち時間30分以上</span></span>
</div>
</div>
'''
st.markdown(legend_html, unsafe_allow_html=True)

# 混雑スポット選択時に分散来訪メッセージ
selected_congested = [s for s in selected_spots if s["congestion"] == "混雑"]
if selected_congested and empty_spots:
    alt_names = [s["name"] for s in empty_spots if s["name"] not in [sc["name"] for sc in selected_congested]]
    if alt_names:
        st.warning(f"{', '.join([s['name'] for s in selected_congested])} は現在混雑しています。\n空いている <b>{', '.join(alt_names)}</b> もおすすめです！", icon="⚠️")

st_folium(m, width=700, height=500) 