CHARS_PER_TOKEN = 4
PRICE_PER_MILLION_TOKENS = 3.00
text = input("Paste some text: ")
chars = len(text)
words = len(text.split())
tokens = round(chars / CHARS_PER_TOKEN)
cost = tokens / 1_000_000 * PRICE_PER_MILLION_TOKENS
print(f"Characters: {chars}")
print(f"Words: {words}")
print(f"Estimated tokens: {tokens}")
print(f"Estimated cost: ${cost:.6f}")