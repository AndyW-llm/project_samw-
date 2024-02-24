SYSTEM_PROMPT="You are a helpful AI bot that answers questions for a user. Keep your response short and direct."
PREFIX_TEMPLATE = "{system_prompt}{content_separator}\n<context>\n{context}\n</context>{content_separator}"
PROMPT_TEMPLATE = "{prefix}\n{question}{eos_symbol}{base_model_modifier}"

content_separators = {
  "NousResearch/Nous-Capybara-34B": "</s><|im_end|>\n<|im_start|>user",
}

EOS_symbols = {
  "NousResearch/Nous-Capybara-34B": "</s>",
  "LargeWorldModel/LWM-Text-Chat-128K": "</s>",
}

BASE_MODEL_modifiers = {
  "LargeWorldModel/LWM-Text-Chat-128K": "ASSISTANT:",
}

def _format_messages(prompt):
    messages = [{"role": "user", "content": prompt}]
    return messages

def format_prompts(
      model_name="",
      context="",
      questions=[],
      
    ):
    if model_name not in content_separators.keys():
      content_separator = ""
    else:
      content_separator = content_separators[model_name]

    if model_name not in EOS_symbols.keys():
      EOS_symbol = ""
    else:
      EOS_symbol = EOS_symbols[model_name]

    if model_name not in BASE_MODEL_modifiers.keys():
      base_model_modifier = ""
    else:
      base_model_modifier = BASE_MODEL_modifiers[model_name]

    prefix = PREFIX_TEMPLATE.format(
      system_prompt=SYSTEM_PROMPT,
      context=context,
      content_separator=content_separator,
    )

    prompts = []
    for question in questions:
      prompts.append(
        PROMPT_TEMPLATE.format(
        prefix=prefix,
        question=question,
        eos_symbol=EOS_symbol,
        base_model_modifier=base_model_modifier,
        )
      )
    return prompts
