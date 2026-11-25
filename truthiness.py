text = input("paste text: ")
if not text:
    print("You didn't paste anything.")
else:
    print(f"Thanks, that's {len(text)} characters.")