import os
import json
import re
from langdetect import detect

folder = "youtube/documents"
old_folder = "youtube/transcripts"
length_filter = 50

def getNum(number):
    number = number.replace(",","").split(" ")[0]
    number = number.split("K")
    if len(number) == 2:
      number = float(number[0])*1000
    else:
        number = number[0]
        number = number.split("M")
        if len(number) == 2:
          number = float(number[0])*1000000
        else:
          number = number[0]
    if number is "" or number is "No":
      number = 0
    try:
      number = int(number)//1
    except:
      number=0
    return number

def getDate(date):
    matches = re.findall(r"(\w\w\w\s\d?\d,\s\d\d\d\d)",date)
    if len(matches) < 1:
      return date
    return matches[0]

def getSeconds(time):
    time = re.findall(r"(\d\d):(\d\d)",time)
    return int(time[0][0])*60+int(time[0][1])

vidnum=0

if not os.isdir("youtube")
    mkdir("youtube")
if not os.isdir("youtube/documents")
    mkdir("youtube/documents")

for filename in os.listdir(old_folder):
    vidnum+=1
    if vidnum > 0:
      print(filename+"-"+str(vidnum))
      f = open(old_folder + "/" + filename,"r")
      vid = f.read()
      f.close()
      vid = vid.replace('\r','\n')
      vid = vid.split("<<~~ Transcript ~~>>")
      if len(vid) == 1:
          continue
      no_metadata = True
      no_english = True
      metadata = vid[0]
      vid = vid[1:]
  
      metadata = metadata.split("<<~~ Metadata ~~>>")

      if len(metadata) > 1:
          no_metadata = False
          metadata = metadata[1]
          description = metadata.split("<<~~ Description ~~>>")
          metadata = description[0].split('\n')
          description = description[1]
          category = description.split("<<~~ Category ~~>>")
          description = category[0]
          category = category[1]
          title = metadata[1]
          owner = metadata[2]
          subscribers = getNum(metadata[3])
          comments = getNum(metadata[4])
          views = getNum(metadata[5])
          likes = getNum(metadata[6])
          dislikes = getNum(metadata[7])
          data = getDate(metadata[8])
  
      i = 0
      length = 0
      too_short = False
      for transcript in vid:
          matches = re.findall(r"(\d\d:\d\d)",transcript)
          if len(matches) > 0:
            length = getSeconds(matches[-1])
          transcript = re.sub(r"\d\d:\d\d"," ",transcript)
          transcript = re.sub(r"\n"," ",transcript)
          transcript = re.sub(r'\[.+?\]'," ",transcript)
          transcript = re.sub(r"\s+"," ",transcript).strip()
          try:
              lang = detect(transcript)
          except:
              lang = "NONE"
          if str(lang) == "en":
              vid = transcript
              if len(vid.split(" ")) < length_filter:
                  too_short = True
              no_english = False
              break
          i+=1
  
      vid = "\n<<~~ Transcript ~~>>\n".join(vid)
  
      new_filename = folder + "/"
      if no_english or no_metadata or too_short:
          vidnum = vidnum-1
          continue
      else:
  
          description = re.sub(r"\n"," ",description)
          description = re.sub(r"\s+"," ",description).strip()
          metadata += str(vidnum)
          metadata += "\t" + filename.split(".txt")[0]
          metadata += "\t" + title
          metadata += "\t" + owner
          metadata += "\t" + description
          metadata += "\t" + str(subscribers)
          metadata += "\t" + str(comments)
          metadata += "\t" + str(views)
          metadata += "\t" + str(likes)
          metadata += "\t" + str(dislikes)
          metadata += "\t" + str(data)
          metadata += "\t" + str(length)
  
          category = category.split("\n")[1:-1]
          j = 0
          for i in range(0, len(category)):
            if category[i] is "Learn More":
              j+=1
              continue
            if (i+j)%2 is 0:
              heading = category[i]
            else:
              meta += "\t<<~~ "+heading+" ~~>> " + category[i]
            

          metadata += "\n"


      f = open(folder + "/"+str(vidnum)+".txt", "w")
      
      f.write(vid)
      
      f.close()
      f = open(folder + "/metadata.txt","a")
      f.write(metadata)
      f.close()



