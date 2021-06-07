import os

import karateclub
import matplotlib.pyplot as plt
import networkx as nx


def make_graph(path):
    G = nx.Graph()
    index = 0
    index2id = dict()
    id2index = dict()

    def add_node(node: str):
        id = int(node.split(' ')[-1])
        index = id2index[id]
        G.add_node(index)
        G.nodes[index]['id'] = id  # 在属性中保存id

    def add_edge(source: str, target: str):
        source_id = int(source.split(' ')[-1])
        target_id = int(target.split(' ')[-1])
        G.add_edge(id2index[source_id], id2index[target_id])

    with open(path, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        # 建立id和index之间映射
        for i in range(len(lines)):
            if lines[i].startswith('id'):
                id = int(lines[i].split(' ')[-1])
                index2id[index] = id
                id2index[id] = index
                index += 1
        # 构建图
        for i in range(len(lines)):
            if lines[i].startswith('id'):
                add_node(lines[i])
            if lines[i].startswith('source'):
                add_edge(lines[i], lines[i + 1])
    return G


def community_detection(G, method='EgoNetSplitter'):
    model_dict = {
        # Overlapping Community Detection
        'DANMF': karateclub.DANMF,
        'MNMF': karateclub.MNMF,
        'EgoNetSplitter': karateclub.EgoNetSplitter,
        'NNSED': karateclub.NNSED,
        'BigClam': karateclub.BigClam,
        'SymmNMF': karateclub.SymmNMF,
        # Non-Overlapping Community Detection
        'GEMSEC': karateclub.GEMSEC,
        'EdMot': karateclub.EdMot,
        'SCD': karateclub.SCD,
        'LabelPropagation': karateclub.LabelPropagation,
    }
    model = model_dict[method]()
    model.fit(G)
    member_community = model.get_memberships()
    for index, community in member_community.items():
        G.nodes[index]['community'] = community
    return member_community


def show_result(G, method='EgoNetSplitter'):
    member_community = community_detection(G, method)

    # 图的布局
    pos = nx.spring_layout(G)

    # 社区发现前
    nx.draw(G, pos, node_size=200, node_color='g', alpha=0.6)
    node_id = nx.get_node_attributes(G, 'id')
    nx.draw_networkx_labels(G, pos, labels=node_id)
    plt.savefig("./graph.png")
    plt.show()

    # 社区发现后
    community = set()
    for values in member_community.values():
        if type(values) == list:
            community.update(values)
        else:
            community.add(values)
    # #000000 ~ #FFFFFF
    color_list = ['Blue', 'Green', 'Yellow', 'Gold', 'Orange', 'Red', 'Brown', 'Gray', '#6B8E23', 'Pink', 'Purple',
                  '#87CEEB', '#00FFFF', '#008080', '#7FFFAA', '#8FBC8F', '#6495ED', '#1E90FF', '#4B0082', '#DB7093',
                  '#EE82EE']
    index = 0
    for com in community:
        list_nodes = list()
        for node, value in member_community.items():
            if type(value) == list:
                if com in value:
                    list_nodes.append(node)
            else:
                if com == value:
                    list_nodes.append(node)
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size=200, node_color=color_list[index], alpha=0.6)  # 画点
        index += 1
    node_community = nx.get_node_attributes(G, 'community')
    nx.draw_networkx_labels(G, pos, labels=node_community)  # 画点（加label）
    nx.draw_networkx_edges(G, pos)  # 画边
    plt.savefig("./result.png")
    plt.show()


if __name__ == '__main__':
    if os.path.exists('./karate.gml'):
        path = './karate.gml'
    elif os.path.exists('./作业3数据集.txt'):
        path = './作业3数据集.txt'
    else:
        print('未找到数据集')
        exit(1)
    G = make_graph(path)
    # 重叠社区发现方法：'DANMF', 'MNMF', 'EgoNetSplitter', 'NNSED', 'BigClam', 'SymmNMF'
    # 非重叠社区发现方法：'GEMSEC', 'EdMot', 'SCD', 'LabelPropagation'
    show_result(G, method='BigClam')
