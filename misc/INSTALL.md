# NOTES for `project_samw*` installation

## Installation Steps
1. **Install the project**
```bash
conda create -n samw python=3.10
conda activate samw
git clone https://github.com/AndyW-llm/project_samw-.git
cd project_samw-
pip install -e .
```

2. **Run the project**
```bash
cd project_samw-
samw
```

3. **Enter Config Information**: 

- If you don't have one, you can obtain an OpenAI key [here](https://platform.openai.com/account/api-keys)
<div align="center">
  <img src="https://github.com/OthersideAI/self-operating-computer/blob/main/readme/key.png" width="300"  style="margin: 10px;"/>
</div>

- You will also need to provide path to your `knowledge` and `index` folder.

4. **Give Terminal app the required permissions**: As a last step, the Terminal app will ask for permission for "Screen Recording" and "Accessibility" in the "Security & Privacy" page of Mac's "System Preferences".

<div align="center">
  <img src="https://github.com/OthersideAI/self-operating-computer/blob/main/readme/terminal-access-1.png" width="300"  style="margin: 10px;"/>
  <img src="https://github.com/OthersideAI/self-operating-computer/blob/main/readme/terminal-access-2.png" width="300"  style="margin: 10px;"/>
</div>