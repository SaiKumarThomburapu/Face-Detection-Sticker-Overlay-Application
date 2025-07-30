import numpy as np
from sklearn.cluster import DBSCAN

def cluster_embeddings(faces, eps=0.6, min_samples=3):
    embeddings = np.array([f["embedding"] for f in faces])
    db = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine").fit(embeddings)
    labels = db.labels_
    clustered = {}
    for i, lbl in enumerate(labels):
        if lbl == -1:
            continue
        clustered.setdefault(lbl, []).append(faces[i])
    return clustered


