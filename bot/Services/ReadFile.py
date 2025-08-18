async def read_file(input_text):
    with open(f"bot/Templates/text/{input_text}.txt", 'r', encoding='utf-8') as file:
        text = file.read()
    return text