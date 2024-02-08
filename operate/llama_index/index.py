"""
index documents or load index
"""

import argparse
import os
import llama_index


def define_knowledge_index_path(knowledge_folder_name='paul_graham'):
  PRJ_DIR = os.getcwd()
  doc_path = os.path.join(PRJ_DIR, 'knowledge', knowledge_folder_name)
  idx_path = os.path.join(PRJ_DIR, 'index',knowledge_folder_name)
  return(doc_path, idx_path)


def load_index(
    idx_path="./storage", 
  ):
  """
  example usage:
  _, idx_path = define_knowledge_index_path(knowledge_folder_name="leethub_v2")
  index = load_index(idx_path=idx_path)
  """
  storage_context = llama_index.StorageContext.from_defaults(persist_dir=idx_path)
  index = llama_index.load_index_from_storage(storage_context=storage_context)
  print(f"set up vector store from storage {idx_path}: SUCCESS")
  return(index)


def build_index(
    doc_path="./doc", 
    idx_path="./storage", 
    export_idx=True,
    required_exts=[".md", ".json", ".py"],
    recursive=True,
    index_mode="bm25",
  ):
  docs = llama_index.SimpleDirectoryReader(
    input_dir=doc_path,
    required_exts=required_exts,
    recursive=recursive,
  ).load_data()
  print(f"load_doc from {doc_path}: SUCCESS")

  index = None
  nodes = None
  service_context = None
  if index_mode in ["bm25", "hybrid"]:
    from llama_index.llms import OpenAI
    llm = OpenAI(model="gpt-4")
    service_context = llama_index.ServiceContext.from_defaults(chunk_size=1024, llm=llm)
    nodes = service_context.node_parser.get_nodes_from_documents(docs)
    if index_mode == "hybrid":
      storage_context = llama_index.StorageContext.from_defaults()
      storage_context.docstore.add_documents(nodes)
      index = llama_index.VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        service_context=service_context,
      )
  else:
    index = llama_index.VectorStoreIndex.from_documents(docs)
    print(f"set up vector store index: SUCCESS")
  if index and export_idx:
    index.storage_context.persist(persist_dir=idx_path)
    print(f"persist vector store index: SUCCESS")
  return index, nodes, service_context


def index_docs():
  parser = argparse.ArgumentParser(
      description="Index docs or load index."
  )
  parser.add_argument(
      "-k",
      "--knowledge",
      help="Specify which knowledge base to read",
      required=False,
      default="leethub_v2", # 'paul_graham'
  )
  
  args = parser.parse_args()
  doc_path, idx_path = define_knowledge_index_path(knowledge_folder_name=args.knowledge)
  
  # TODO: add export_idx, required_exts, recursive arguments.
  index, _ = build_index(
    doc_path=doc_path, 
    idx_path=idx_path, 
    export_idx=True,
    required_exts=[".md", ".py"],
    recursive=True,
    index_mode="bm25",
  )
  # TODO: test index, print example query result.
  return()


if __name__ == "__main__":
  # from source.config.settings import Config
  # config = Config()
  # print("OPENAI_API_KEY: ", os.environ["OPENAI_API_KEY"])
  raise ValueError("Yet to debug index procedure.")
  # index_docs()
