"""
prepare query engine
"""
import os
from operate.llama_index.index import load_index, build_index
import llama_index
from llama_index.schema import QueryBundle
from llama_index.retrievers import BM25Retriever
from llama_index.retrievers import BaseRetriever
from llama_index.query_engine import RetrieverQueryEngine

class HybridRetriever(BaseRetriever):
  def __init__(self, vector_retriever=None, bm25_retriever=None):
    self.vector_retriever = vector_retriever
    self.bm25_retriever = bm25_retriever
    super().__init__()

  def _retrieve(self, query, **kwargs):
    nodes = None
    if self.bm25_retriever:
      bm25_nodes = self.bm25_retriever.retrieve(query, **kwargs)
      nodes = bm25_nodes
    if self.vector_retriever:
      vector_nodes = self.vector_retriever.retrieve(query, **kwargs)
      nodes = bm25_nodes+vector_nodes if nodes else vector_nodes

    # combine the two lists of nodes
    all_nodes = []
    node_ids = set()
    for n in nodes:
      if n.node.node_id not in node_ids:
        all_nodes.append(n)
        node_ids.add(n.node.node_id)
    return all_nodes


def get_custom_retriever(index, nodes, top_k=2):
  vector_retriever, bm25_retriever = None, None
  if index:
    vector_retriever = index.as_retriever(similarity_top_k=top_k)
  if nodes:
    bm25_retriever = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=top_k)
  return vector_retriever, bm25_retriever


def get_reranker(top_n=4, model="BAAI/bge-reranker-base"):
  from llama_index.postprocessor import SentenceTransformerRerank
  reranker = SentenceTransformerRerank(top_n=top_n, model=model)
  return reranker


# TODO: setup as service
def get_query_engine(
  knowledge_dir = None,
  index_dir = None,
  knowledge = "leethub_v2",
  response_mode = "no_text", # "compact"
  streaming = False,
  index_mode="bm25",
):
  doc_path = os.path.join(knowledge_dir, knowledge)
  idx_path = os.path.join(index_dir, knowledge)

  if index_mode == "bm25":
    # see https://docs.llamaindex.ai/en/stable/examples/retrievers/bm25_retriever.html
    index, nodes, service_context = build_index(
      doc_path=doc_path, 
      idx_path=idx_path, 
      export_idx=True,
      required_exts=[".md", ".py"],
      recursive=True,
      index_mode="bm25",
    )
    _, bm25_retriever = get_custom_retriever(index, nodes)

    return(bm25_retriever)
    # from llama_index.retrievers import RouterRetriever
    # from llama_index.tools import RetrieverTool
    # retriever = RouterRetriever.from_defaults(
    #   retriever_tools=[
    #     RetrieverTool.from_defaults(
    #       retriever=bm25_retriever,
    #       description="Useful if searching about specific information",
    #     ),
    #   ],
    #   service_context=service_context,
    #   select_multi=True,
    # )
    # return(retriever)

    # hybrid_retriever = HybridRetriever(vector_retriever, bm25_retriever)
    # # reranker = get_reranker(model="BAAI/bge-reranker-base")
    # # nodes = hybrid_retriever.retrieve(
    # #     "What is the impact of climate change on the ocean?"
    # # )
    # # reranked_nodes = reranker.postprocess_nodes(
    # #     nodes,
    # #     query_bundle=llama_index.QueryBundle(
    # #         "What is the impact of climate change on the ocean?"
    # #     ),
    # # )
    # # TODO: from llama_index.response.notebook_utils import display_source_node
    # # for node in reranked_nodes:
    # #   display_source_node(node)
    # query_engine = RetrieverQueryEngine.from_args(
    #   retriever=hybrid_retriever,
    #   # node_postprocessors=[reranker],
    #   service_context=service_context,
    # )
  else:
    # see https://docs.llamaindex.ai/en/stable/understanding/querying/querying.html
    index = load_index(idx_path=idx_path)
    query_engine = index.as_query_engine(
      streaming=streaming,
      response_mode=response_mode,
    )
    
  return(query_engine)


# TODO: set up as service request
def retrieve(
  llama_idx_engine = None,
  prompt = "What did the author do growing up?",
  index_mode = "bm25",
):
  assert llama_idx_engine is not None
  if index_mode == "bm25":
    response = None
    # source_nodes = llama_idx_engine.retrieve(prompt)
    source_nodes = llama_idx_engine._retrieve(QueryBundle(query_str=prompt))
  else:
    response = llama_idx_engine.query(prompt)
    source_nodes = response.source_nodes
  return response, source_nodes
