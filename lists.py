files = ["contract.txt", "policy.txt"]
files.append("report.txt")  #add to the end
print(len(files))   # how many items
print(files[0])     #the first item
print(files[-1])    # the last item
print(files[0:2])    # the first two
if "policy.txt" in files:
    print("Policy included")
words = "tokens drive the bill".split()
print(words)