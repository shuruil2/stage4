from flask import Flask, jsonify, render_template
import osmnx as ox
import networkx as nx
from shapely.geometry import Point
import folium
from shapely.geometry import LineString
from shapely.ops import unary_union
import pandas as pd
import numpy as np
import json5

app = Flask(__name__)

# 设置OSMnx
ox.config(use_cache=True, log_console=True)

# 定义地点和坐标
place = "Los Angeles, California, USA"
start = (34.063932, -118.359229)  # 例如：洛杉矶艺术博物馆（LACMA）
end = (34.134115, -118.321548)    # 例如：好莱坞标志

# 获取地区的街道网络
G = ox.graph_from_place(place, network_type='drive')

# 找到最近的节点
start_node = ox.distance.nearest_nodes(G, start[1], start[0])
end_node = ox.distance.nearest_nodes(G, end[1], end[0])

# 存储多条路径及其经纬度信息
paths_coords = []

for _ in range(5):  # 生成5条路径
    # 计算最短路径
    route = nx.shortest_path(G, start_node, end_node, weight='length')

    # 提取经纬度信息
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
    paths_coords.append(route_coords)

    # 增加这条路径上所有边的权重
    for i in range(len(route) - 1):
        if G.has_edge(route[i], route[i + 1]):
            G[route[i]][route[i + 1]][0]['length'] *= 1.1

# 打印每条路径的经纬度信息
#for i, coords in enumerate(paths_coords):
#    print(f"Path {i + 1}:")
#    for coord in coords:
#        print(coord)

# 创建初始地图，以第一条路径的起点为中心
map = folium.Map(location=[start[0], start[1]], zoom_start=13)

# 为每条路径绘制一条线
for i, route_coords in enumerate(paths_coords):
    # 为每条路径设置不同的颜色
    line = folium.PolyLine(route_coords, weight=2, color=f'blue', opacity=0.7).add_to(map)
    folium.Marker(route_coords[0], popup=f'Start Path {i+1}').add_to(map)
    folium.Marker(route_coords[-1], popup=f'End Path {i+1}').add_to(map)


# 显示地图
#map_dict = map.to_dict()
map_html = map.get_root().render()

# 定义 Flask 路由

@app.route('/run_script', methods=['GET'])
#@app.route("/")
def run_script():

    #map_html = json5.dumps(map_dict)

    #print("Map HTML:", map_html)

    # 返回 JSON 格式的结果
    return render_template("home.html", map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
