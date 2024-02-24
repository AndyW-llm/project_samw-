from typing import List
from pathlib import Path
from llama_index.readers.file import PyMuPDFReader #llama_index==0.10.4
import os
import re
import requests

def pdf_workflow(
  input_string: str,
  prompt_template: str = "{content}",
):
   if _is_url_or_path(input_string) == "URL":
      file_path = _download_pdf(input_string, folder='./tmp')
   elif _is_url_or_path(input_string) == "File Path":
      file_path = input_string
   query = extract_pdf(file_path, prompt_template)
   return query

def extract_pdf(
  file_path:str, 
  prompt_template:str = "Content:\n{content}"
  ) -> List[str]:
  """
  Extract contents from pdf, and formulate prompt.
  """

  if not os.path.isfile(file_path):
    raise ValueError(f"{file_path} do not exist. Make sure you downloaded the file.")
  
  assert file_path.endswith('.pdf')

  documents = _pdf2txt(file_path)
  contents = _combine_pages(documents, max_length_per_doc=None)
  # TODO: for content in contents:
  query = prompt_template.format(content=contents[0])
  return query


def _download_pdf(url, folder='./tmp'):
    os.makedirs(folder, exist_ok=True)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = url.split('/')[-1]
        filepath = os.path.join(folder, filename)

        with open(filepath, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)
        
        print(f"Downloaded '{filename}' to '{folder}'")
        return filepath
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
        return None

def _pdf2txt(file_path):
  print(f"Reading PDF from {file_path}.")
  reader = PyMuPDFReader()
  documents = reader.load(file_path)
  return documents


def _combine_pages(documents, max_length_per_doc=None):
  document_list = []
  if max_length_per_doc is not None:
    raise NotImplementedError("TODO: support max_length_per_doc")
  content = ""
  # TODO: can be enhanced with .format and "\n\n".join
  for page_i, doc in enumerate(documents):
    content += f"Page: {page_i}\nText: {doc.text}\n\n"
  document_list.append(content)
  return document_list

def _is_url_or_path(input_string):
    # Regex pattern for a basic URL
    url_pattern = re.compile(
        r'^(https?|ftp):\/\/'  # http:// or https:// or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:\/\S*)?$', re.IGNORECASE)  # rest of url

    # Check if it's a URL
    if url_pattern.match(input_string):
        return "URL"
    
    # Check if it's likely a file path
    # This is a simple heuristic and might not cover all cases.
    if "\\" in input_string or "/" in input_string or ":" in input_string:
        return "File Path"
    
    return "Unknown"


if __name__ == "__main__":
  # FILE_PATH="/Users/andywong/Downloads/2. NHD Report.pdf" # 56 pages
  # FILE_PATH="/Users/andywong/Downloads/20240128_AndyWong_Meta_resume (1).pdf" # 1 pages
  FILE_PATH="/Users/andywong/Downloads/Meta-Reports-Fourth-Quarter-and-Full-Year-2023-Results-Initiates-Quarterly-Dividend-2024" # 1 pages
  query = extract_pdf(FILE_PATH)
  print(query)

  


