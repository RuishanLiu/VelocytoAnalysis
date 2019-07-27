import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from .mst import *

def compute_lineage_coorectness(edges_mst, edges):
    def extract_edge(edges):
        return set([(edges[i, 0], edges[i, 1]) for i in range(edges.shape[0])])
    edges = extract_edge(edges)
    edges_mst = extract_edge(edges_mst)
    edges_intersect = edges.intersection(edges_mst)
    correctness = 2 * float(len(edges_intersect)) / (len(edges)+len(edges_mst))
    return correctness

def get_lineage(path, counts, milestones, genes=None, root=None, classifier='rf', n_estimators=50, n_neighbors=3):
    '''
    clssifier: 'rf'(random forest) / 'knn' (k-nearest-neighbors)
    '''
    x = counts if genes is None else counts[:, genes]
    milestones_set = np.sort(list(set(list(milestones))))
    
    # Build classifier for milestons
    if classifier == 'rf':
        classifier_milestone = RandomForestClassifier(n_estimators=n_estimators, random_state=0).fit(x, milestones) 
    elif classifier == 'knn':
        classifier_milestone = KNeighborsClassifier(n_neighbors=n_neighbors, weights='distance').fit(x, milestones) 
        
    # Build graph
    arcs = []
    for i_m, m in enumerate(milestones_set):
        inds = np.arange(milestones.shape[0])[milestones==m]
        path_check = path[:, inds, :]
        trajectory = path_check.transpose(1, 0, 2)
        prob = classifier_milestone.predict_proba(trajectory.reshape(-1, trajectory.shape[2]))
        prob = prob.reshape(trajectory.shape[0], trajectory.shape[1], len(milestones_set)) 
        prob_mean = np.mean(prob, axis=0)
        for i_to, m_to in enumerate(milestones_set):
            if m == m_to:
                continue
            weight = 1 - np.mean(prob_mean[:, i_to])
            arcs.append(Arc(m_to, weight, m))
        
    # Find root
    if root is None:
        prob_in = {}
        prob_out = {}
        for m in milestones_set:
            prob_in[m] = 0
            prob_out[m] = 0
        for arc in arcs:
            node_in, weight, node_out = arc
            prob_out[node_out] += 1-weight
            prob_in[node_in] += 1-weight
        root = min(prob_in, key=prob_in.get)
        print('Root is', root)
        
    # MST
    arcs_mst = min_spanning_arborescence(arcs, root)
    edges_mst = set()
    for arc in arcs_mst.keys():
        node_in, weight, node_out = arcs_mst[arc]
        edges_mst.add((node_out, node_in))
    return np.array(list(edges_mst))
    

