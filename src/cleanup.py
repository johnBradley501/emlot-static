import re
import os


dirbase = "D:/projects/emLoT/emlot.library.utoronto.ca/emlot.library.utoronto.ca"

def doCleanup(text):
    rslt = text
    # rslt = re.sub(r'<!--.*?-->', r'', text, count = 1, flags = re.DOTALL) # removes all commented out stuff
    rslt = re.sub(r'\s*<ul class="utl">.*?Register.*?\</ul>\s*', r'<ul class="utl"><li>&nbsp;</li></ul>', rslt, count = 1, flags = re.DOTALL) # removes Register and Login links from right end
    rslt = re.sub(r'\s*<li class="child[ a-z]*?">\s*?<a href="[\./]*workspace.*?Workspace.*?</li>\n?', r'', rslt, count = 1, flags = re.DOTALL) # removes Workspace from top menu
    rslt = re.sub(r'\s*<li class="child[ a-z]*?">\s*?<a href="[\./]*learning.*?Learning Zone.*?</li>\n?', r'', rslt, count = 1, flags = re.DOTALL) # removes Learning Zone from top menu
    rslt = re.sub(r'\s*<li class="child s[a-z]+">\s*?<a href="[\./]*index.*?Record</a>.*?</li>\n?', r'', rslt, count = 1, flags = re.DOTALL) # removes Record from 2nd menu
    return rslt

def doFile(fn):
    if fn.endswith("html"):
            f = open(fn, "r",encoding='utf-8')
            txt = f.read()
            f.close()

            txt = doCleanup(txt)

            f = open(fn, "w", encoding='utf-8')
            f.write(txt)
            f.close()

for (cur, dirs, files) in os.walk(dirbase, topdown=True):
    cur = re.sub(r"\\",r"/",cur)
    print("Cur: ",cur)
    for fn in files:
        doFile(cur+"/"+fn)