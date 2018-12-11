import folium
from folium import plugins

heatmap_map = folium.Map(location=[51.67109, -1.28278], zoom_start=2)
with open('data.txt','r') as f:
    for row in f:
        data = row.strip().split(',')
        data = [[[data[0],data[1]]]
        #print(data)
        hm = plugins.HeatMap(data)
        heatmap_map.add_child(hm)

f.close()

heatmap_map.save("heatmap.html")
