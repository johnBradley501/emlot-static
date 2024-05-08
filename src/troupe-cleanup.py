import re
import os


dirbase = "D:/projects/emLoT/emlot.library.utoronto.ca/emlot/db/record/troupe"

def doCleanup(text):
    if not re.findall(r"Patrons and Performances Web Site", text):
        return ""
    rslt = text
    rslt = re.sub(r'\s*\(Links to REED Patrons and Performances Web Site\)', r'', rslt, flags = re.DOTALL) # removes Record from 2nd menu
    rslt = re.sub(r'<a href="http\://link\.library\.utoronto\.ca/reed/patron\.cfm\?PeopleListID=.*?>(.*?)</a>', r'\1', rslt, flags = re.DOTALL) # removes Record from 2nd menu
    rslt = re.sub(r'<a href="http\://link\.library\.utoronto\.ca/reed/troupe\.cfm\?TroupeListID=.*?>(.*?)</a>', r'\1', rslt, flags = re.DOTALL) # removes Record from 2nd menu
    return rslt


def doFile(fn):
    if fn.endswith("html"):
            f = open(fn, "r",encoding='utf-8')
            txt = f.read()
            f.close()

            txt = doCleanup(txt)
            if not txt:
                return

            f = open(fn, "w", encoding='utf-8')
            f.write(txt)
            f.close()

for (cur, dirs, files) in os.walk(dirbase, topdown=True):
    cur = re.sub(r"\\",r"/",cur)
    print("Cur: ",cur)
    for fn in files:
        doFile(cur+"/"+fn)

print("Done!")
