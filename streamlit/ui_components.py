# PDF renderer
import base64
import os
# Full PDF viewer / Overview
def encodePDF(file_path=None):
    
    if file_path is None:
      return "## PDF will be shown here."
    elif not os.path.isfile(file_path):
      return f"Import PDF error! Can't find {file_path}."
    
    # Opening file from file path
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_encoded =  f"""<embed
    class="pdfobject"
    type="application/pdf"
    title="Embedded PDF"
    src="data:application/pdf;base64,{base64_pdf}"
    style="overflow: auto; width: 100%; height: 100%;">"""

    return(pdf_encoded)

# Left hidden menu
hidden_sidebar_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
</style>
"""

# Footer message
modify_footer_js="""
<script>
window.parent.document.getElementsByTagName("footer")[0].innerHTML={footer_mesage}
</script>
"""

from streamlit.components.v1 import html
def scroll2input():
    html(
    """
    <script>window.parent.document.getElementsByTagName("textarea")[0].scrollIntoView();</script>
    """,
    height=2
    )