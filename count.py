s=input()
count={}
for char in s:
    if char in count:
        count[char]+=1
    else:
        count[char]=1
print(sorted(count.items(),key=lambda x:x[1], reverse=True))
