string1=input("string 1:")

string2=input("string 2:")

count=0

for i in string1:

    for j in string2:

        if i==j:

            count=count+1

if count==len(string1):

    print("Strings are anagram of each other.")

else:
    print("Strings are not anagram of each other.")
