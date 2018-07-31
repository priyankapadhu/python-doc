n=int(input("enter number of elements"))
b=[]
for i in range(0,n):
  ele=int(input("enter the element"))
  b.append(ele)
avg=sum(b)/number
print("average=" , round(avg,2))
