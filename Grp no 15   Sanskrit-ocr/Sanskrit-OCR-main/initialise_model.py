from cgitb import text
import easyocr
import translators as ts
import os


def easy_model(finallist):
    # print("Length: ",len(finallist[0]))
    if len(finallist[0])==0:
        print("easy_model: No images in folder! Exiting...")
        return
    else:
        reader = easyocr.Reader(['en','hi'])
        images = finallist[0]
        count = finallist[1]
        for i in range(len(images)):
            filename = r"images/"+"{}".format(images[i])
            # print("Image {}:".format(i), filename)
            output = reader.readtext(filename, paragraph=True, batch_size=3)
            sans_text = ""
            for j in range(len(output)):
                sans_text = sans_text+" \n"+output[j][1]
            translated_text = ts.google(query_text=sans_text,to_language='en')
            # print("\n\n\n\n Page {}".format(i),translated_text)

            #save to text file
            textfilename = os.path.splitext(images[i])[0].lower()
            with open(r'results/{}.txt'.format(textfilename), 'w',encoding="utf-8") as f:
                f.write(translated_text)
            print("Percentage: "+str(round(((i+1)/len(images))*100,2))+"%\r",end="")
        input("Task successfully completed! Press Enter to quit...")