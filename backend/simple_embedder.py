"""
Simple embedding using TF-IDF (no external API needed, completely free).
This is a fallback for when API-based embeddings are unavailable.
"""
import hashlib
import math
from collections import Counter
from typing import List


class SimpleEmbedder:
    """
    Creates embeddings using TF-IDF (Term Frequency-Inverse Document Frequency).
    This is a simple, fast, and completely free alternative that works offline.
    """
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.idf_cache = {}
        self.all_docs = []
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        # Store documents for IDF calculation
        self.all_docs.extend(texts)
        
        embeddings = []
        for text in texts:
            embedding = self._text_to_embedding(text)
            embeddings.append(embedding)
        
        return embeddings
    
    def _text_to_embedding(self, text: str) -> List[float]:
        """Convert text to a fixed-size embedding vector."""
        # Tokenize and count words
        words = text.lower().split()
        word_counts = Counter(words)
        
        # Calculate TF-IDF scores
        tf_idf_scores = {}
        total_words = len(words)
        
        for word, count in word_counts.items():
            # Term Frequency
            tf = count / total_words if total_words > 0 else 0
            
            # Inverse Document Frequency (simplified)
            idf = self._get_idf(word)
            
            tf_idf_scores[word] = tf * idf
        
        # Create fixed-size embedding using hashing
        embedding = [0.0] * self.dimension
        
        for word, score in tf_idf_scores.items():
            # Hash word to get indices
            hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16)
            idx1 = hash_val % self.dimension
            idx2 = (hash_val // self.dimension) % self.dimension
            
            # Distribute score across multiple dimensions
            embedding[idx1] += score
            embedding[idx2] += score * 0.5
        
        # Normalize to unit vector
        magnitude = math.sqrt(sum(x * x for x in embedding))
        if magnitude > 0:
            embedding = [x / magnitude for x in embedding]
        
        return embedding
    
    def _get_idf(self, word: str) -> float:
        """Calculate IDF for a word (simplified version)."""
        if word in self.idf_cache:
            return self.idf_cache[word]
        
        # Count documents containing the word
        doc_count = sum(1 for doc in self.all_docs if word in doc.lower())
        
        # Calculate IDF
        total_docs = len(self.all_docs) if self.all_docs else 1
        idf = math.log((total_docs + 1) / (doc_count + 1)) + 1
        
        self.idf_cache[word] = idf
        return idf
