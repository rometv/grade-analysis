import re

string = "Point groups: " \
         "[AVL operatsioonid]: 0.0/2.0 (0.0/12.5) " \
         "[Puude ühendamine]: 0.6666666666666666/1.0 (4.0/6.0) " \
         "Grade :=>> 17.778"
point_groups = re.search(r'(?<=(Point groups: ))(\[.*?\].*)', string)
print(f'"{point_groups.group()}"')
point_groups = re.findall(r'(?<=\[)(.*?)(?=\]:)', point_groups.group(), flags=re.M)
print(point_groups)
