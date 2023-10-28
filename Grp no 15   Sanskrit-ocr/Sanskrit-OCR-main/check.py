import os
def checkimages():
    removelist=[]
    finallist=[]
    print("\nFile types supported are jpg and png! Others will be ignored.\n")
    path = r"images/"
    a=os.listdir(path)
    count=0
    for i in a:
        # print(a)
        ext = os.path.splitext(i)[-1].lower()
        # Now we can simply use == to check for equality, no need for wildcards.
        if ext == ".jpg" or ext=='.png':
            # print (i, "can be used")
            count= count+1
        else:
            print (i, "cannot be used. Ignored!")
            removelist.append(i)
    for i in a[:]: #removing files which are not jpg..
        if i in removelist:
            a.remove(i)
    if count==0:
        print("No jpg file in images. Please try again!")
        return
    else:
        print("\n\nFound {} image file(s) in total. Continuing...".format(count))
        finallist.append(a)
        finallist.append(count)
        return finallist