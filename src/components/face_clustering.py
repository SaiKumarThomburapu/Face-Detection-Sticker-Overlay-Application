import numpy as np
from sklearn.cluster import DBSCAN
from typing import Dict, List
from src.entity.config_entity import ClusteringConfig
from src.entity.artifacts import FaceArtifact, ClusteringArtifacts

class FaceClusteringComponent:
    def __init__(self):
        pass
    
    def cluster_embeddings(self, faces: List[FaceArtifact], config: ClusteringConfig) -> ClusteringArtifacts:
        """Cluster face embeddings using DBSCAN"""
        if not faces:
            return ClusteringArtifacts(
                clusters={},
                cluster_count=0,
                noise_faces=0
            )
        
        embeddings = np.array([f.embedding for f in faces])
        db = DBSCAN(eps=config.eps, min_samples=config.min_samples, metric=config.metric).fit(embeddings)
        labels = db.labels_
        
        clustered = {}
        noise_count = 0
        
        for i, lbl in enumerate(labels):
            if lbl == -1:
                noise_count += 1
                continue
            clustered.setdefault(lbl, []).append(faces[i])
        
        # Convert to native int keys
        cleaned_clusters = {}
        for cid, face_list in clustered.items():
            native_cid = int(cid)
            cleaned_clusters[native_cid] = face_list
        
        return ClusteringArtifacts(
            clusters=cleaned_clusters,
            cluster_count=len(cleaned_clusters),
            noise_faces=noise_count
        )

