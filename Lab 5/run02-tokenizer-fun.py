model_path = "dialogpt"

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(model_path, padding_side = "right")
model = AutoModelForCausalLM.from_pretrained(model_path)
model.to("cpu")
model.eval() #Dodałem

inputs = torch.stack([torch.tensor([2061,   338,   534, 12507,  2057,    30,   220, 50256])])
inputs.to("cpu")

outputs = model.generate(inputs, max_length=128, pad_token_id=tokenizer.eos_token_id)
outputs_extracted = outputs[:, inputs.shape[-1]:][0]
answer = tokenizer.decode(outputs_extracted, skip_special_tokens=True)
print("Odpowiedź: {}".format(answer))

outputs_extracted = torch.tensor([40,  1101,   407,   845, 14720,   996,    13,   220, 50256])
answer = tokenizer.decode(outputs_extracted, skip_special_tokens=True)
print("Odpowiedź: {}".format(answer))

