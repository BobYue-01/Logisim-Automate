# %%
import sys
import xml.etree.ElementTree as ET


# %% [markdown]
# 将下面的 `file_dir` 的值改为你的文件相对路径

# %%
file_dir = './sample.circ'


# %% [markdown]
# 由于 Logisim 保存的文件中的元素的顺序是不确定的，所以在自动化重命名之前需要进行排序。
# 
# 此处以 `name` 为主要关键字，`loc` 的 y, x 轴坐标为次要关键字。
# 
# 即意味着，首先按元素的分类排序；对于同类的元素，以行为单位进行排序，同一行中，以列为单位进行排序。
# 

# %%
def sort_comp(elem):
	loc = elem.get('loc')
	if loc is None:
		# no location, sort by name
		return (elem.get('name') or ""), 0, 0
	# loc: str '(x, y)'
	# turn loc to tuple
	loc = tuple(map(int, loc[1:-1].split(',')))
	# sort by y, then x
	return (elem.get('name') or ""), loc[1], loc[0]


# %% [markdown]
# 读入文件，解析为 ElementTree 对象，然后对根节点的子节点进行排序，最后输出到文件 `sorted.circ`。
# 

# %%
# sort sequence XML `comp` items in `project\circuit\` by type and tags; no need to print them.
tree = ET.parse(file_dir)
root = tree.getroot()
for circuit in root.findall('circuit'):
	# sort thier sequence by name
	sorted_circuit = sorted(circuit, key = sort_comp)
	# trun the list into a ET
	new_circuit = ET.Element('circuit', attrib=circuit.attrib)
	for element in sorted_circuit:
		new_element = ET.SubElement(new_circuit, element.tag, attrib=element.attrib)
		for subelement in element:
			ET.SubElement(new_element, subelement.tag, attrib=subelement.attrib).text = subelement.text
			for subsubelement in subelement:
				ET.SubElement(subelement, subsubelement.tag, attrib=elemesubsubelementnt.attrib).text = subsubelement.text
	root.remove(circuit)
	root.append(new_circuit)
# write the sorted tree to a new file
tree.write('./sorted.circ')


# %% [markdown]
# 以下的代码要求待重命名的元素具有 `o_00` 的标签。
# 

# %%
# 按普通文本读取 '.\sorted.circ'，并另存为 '.\renamed.circ'

read_file = open('./sorted.circ', 'r')
new_file = open('./renamed.circ', 'w')
content = read_file.read()

# 递增重命名 'o_00' 为 'o_00' 到 'o_31'

content = content.replace('_00', '_$$')

i = 0
while i < 32:
	content = content.replace('o_$$', 'o_' + str(i).zfill(2), 1)
	i += 1

i = 0
while i < 32:
	content = content.replace('o_$$', 'o_' + str(i).zfill(2), 1)
	i += 1

i = 0
while i < 32:
	content = content.replace('i_$$', 'i_' + str(i).zfill(2), 1)
	i += 1

new_file.write(content)

# %%
read_file.close()
new_file.close()



