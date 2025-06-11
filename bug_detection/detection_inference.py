def predict_detection(tokenizer, model, source, beam_size=5):
    tokenized_inputs = tokenizer(source, padding=True, truncation=True, return_tensors="pt").to(model.device)
    tokenized_labels = model.generate(num_beams=beam_size, no_repeat_ngram_size=2, num_return_sequences=beam_size, **tokenized_inputs).cpu().detach().numpy()
    return tokenizer.batch_decode(tokenized_labels, skip_special_tokens=True)

