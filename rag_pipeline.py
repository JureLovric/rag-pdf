from dataclasses import dataclass
self.vecs = None # (N, D)


def add(self, vecs: np.ndarray):
vecs = vecs.astype("float32")
if self.normalize:
vecs = _l2_normalize(vecs)
if self.vecs is None:
self.vecs = vecs
else:
self.vecs = np.vstack([self.vecs, vecs])


def search(self, q: np.ndarray, k: int):
if self.normalize:
q = _l2_normalize(q.astype("float32"))
if self.vecs is None or self.vecs.shape[0] == 0:
I = -np.ones((q.shape[0], k), dtype=int)
D = np.zeros((q.shape[0], k), dtype="float32")
return D, I
# inner product similarity
sims = q @ self.vecs.T # (1, N)
idx = np.argsort(-sims, axis=1)[:, :k]
val = np.take_along_axis(sims, idx, axis=1)
return val.astype("float32"), idx.astype(int)




@dataclass
class RAGIndex:
model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
normalize: bool = True


def __post_init__(self):
self.emb = SentenceTransformer(self.model_name)
self.dim = self.emb.get_sentence_embedding_dimension()
if faiss is not None:
self.index = faiss.IndexFlatIP(self.dim) if self.normalize else faiss.IndexFlatL2(self.dim)
else:
self.index = _NumpyIPIndex(self.dim, normalize=self.normalize)
self.store: List[str] = []


def _encode(self, texts: List[str]) -> np.ndarray:
vecs = self.emb.encode(texts, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=self.normalize)
return vecs.astype('float32')


def add(self, chunks: List[str]):
if not chunks:
return
vecs = self._encode(chunks)
# faiss IndexFlatIP exposes .add, numpy fallback too
self.index.add(vecs)
self.store.extend(chunks)


def search(self, query: str, k: int = 6) -> List[Tuple[int, float, str]]:
if not self.store:
return []
q = self._encode([query])
D, I = self.index.search(q, k)
res = []
for idx, score in zip(I[0], D[0]):
if idx is None or int(idx) < 0:
continue
res.append((int(idx), float(score), self.store[int(idx)]))
return res
