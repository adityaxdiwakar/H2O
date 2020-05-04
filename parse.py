import json

with open("bin/sample_data.txt", "r") as f:
    data = f.readlines()

depths = []
for line in data:
    line = line[1:]
    depths.append(json.loads(line))

depths = [depth[0]["d"]["doms"][0] for depth in depths]

with open("bin/sample_data.json", "w") as f:
    json.dump(depths, f, indent=2)

