import matplotlib.pyplot as plt
import networkx as nx


def make_graph(path):
    G = nx.Graph()

    def add_edge(source: str, target: str):
        source = int(source.split(' ')[-1])
        target = int(target.split(' ')[-1])
        G.add_edge(source, target)

    with open(path, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        for i in range(len(lines)):
            if lines[i].startswith('source'):
                add_edge(lines[i], lines[i + 1])
    return G


def core_number_1(G):
    # 返回节点核数，字典形式
    node_core = nx.algorithms.core_number(G)
    return node_core


def core_number_2(G):
    # 返回节点核数，字典形式
    degrees = dict(G.degree())
    # Sort nodes by degree.
    nodes = sorted(degrees, key=degrees.get)

    nbrs = {v: list(nx.all_neighbors(G, v)) for v in G}
    max_degree = degrees[nodes[-1]]  # 最大度数

    def deal_core(max, nbrs):

        for i in nbrs:  # 互删
            if len(nbrs[i]) < max:
                nbrs.pop(i)
                for j in nbrs:
                    if i in nbrs[j]:
                        nbrs[j].remove(i)
                deal_core(max, nbrs)
                break
        return list(nbrs.keys())

    cores = {}
    for i in range(1, max_degree):
        x = deal_core(i, nbrs)
        if x == []:
            break
        else:
            cores[i] = x

    core_num = {}
    for i in nodes:
        core_num[i] = 0
        for j in cores:
            if i in cores[j]:
                core_num[i] += 1

    return core_num


def add_to_attr(G, node_core):
    # 将结果添加到属性中
    graph_core = max(node_core.values())  # 图的核数
    print('节点核数: ', node_core)
    print('图的核数: ', graph_core)
    for node, core in node_core.items():
        G.nodes[node]['core'] = core
    G.graph['core'] = graph_core


def show_result(G):
    # circular_layout：节点在一个圆环上均匀分布
    # random_layout：节点随机分布
    # shell_layout：节点在同心圆上分布
    # spring_layout：用Fruchterman - Reingold算法排列节点（样子类似多中心放射状）
    # spectral_layout：根据图的拉普拉斯特征向量排列节点
    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=200, node_color='g', alpha=0.6)
    plt.savefig("./graph.png")
    plt.show()

    nx.draw(G, pos, node_size=200, node_color='g', alpha=0.6)
    node_core = nx.get_node_attributes(G, 'core')
    nx.draw_networkx_labels(G, pos, labels=node_core)
    plt.savefig("./result.png")
    plt.show()


if __name__ == '__main__':
    path = './inputdoc2.gml'
    G = make_graph(path)
    core_num_test = core_number_1(G)
    core_num = core_number_2(G)
    if core_num_test == core_num:
        print('right!')
    else:
        print('wrong!')
    add_to_attr(G, core_num)
    show_result(G)
