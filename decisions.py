tokens = 2000000
if tokens <= 8000:
    size = "small"
elif tokens <= 128000:
    size = "medium"
elif tokens <= 1000000:
    size = "large"
else:
    size = "too big -spilt it up"
print(f"This document is {size}")
