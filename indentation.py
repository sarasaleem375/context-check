tokens = 5000
limit = 8000
split_needed = False
if tokens > limit:
    print("too big")
split_needed = True
print("done")
print(f"split_needed = {split_needed}")
