# ssh -L 8000:localhost:8000 e97
# conda activate qa_demo

# Changing the directory
cd /Users/andywong/andyw/side_projects/project_samw-/streamlit

# Running the codecracker command
export STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true
export TOKENIZERS_PARALLELISM=false
streamlit run ./pdf_QA_app.py