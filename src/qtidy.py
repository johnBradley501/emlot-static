import re
q = """
SELECT DISTINCT ltbapp_document.pubdate_from_year, ltbapp_document.id, ltbapp_document.title
FROM ltbapp_document
WHERE (((ltbapp_document.pubdate_from_year) Is Not Null) AND ((ltbapp_document.document_metatype_id)=3))
ORDER BY ltbapp_document.pubdate_from_year, ltbapp_document.title;
"""
tableData = [
    ["ltbapp_document_prod_auspices", "ispa"],
    ["ltbapp_document_helper_m2mauthors", "m2ma"],
    ["ltbapp_record_src_transcriptionnotes", "rstn"],
    ["ltbapp_ass_event_people_role", "isepr"],
    ["ltbapp_ass_event_people", "isep"],
    ["ltbapp_ass_event_venues", "isev"],
    ["ltbapp_ass_event_troupes", "iset"],
    ["ltbapp_event_event_type", "iseet"],
    ["ltbapp_troupe_typeoftroupe", "istt"],
    ["ltbapp_docauthors", "isda"],
    ["ltbapp_docsecauthors", "isdSa"],
    ["ltbapp_docpublisher", "isdp"],
    ["ltbapp_docrepository", "isdr"],
    ["ltbapp_document_doc_type", "isddt"],
    ["ltbapp_document_doc_class", "isddc"],
    ["ltbapp_venue_helper_m2mlocales", "m2m"],
    ["ltbapp_record_helper_documents", "isrd"],
    ["ltbapp_role", "rl"],
    ["ltbapp_venuename", "vn"],
    ["ltbapp_venue", "ve"],
    ["ltbapp_auspicesproduction", "aus"],
    ["ltbapp_eventtype", "et"],
    ["ltbapp_event", "ev"],
    ["ltbapp_person", "pe"],
    ["ltbapp_publisher", "pub"],
    ["ltbapp_documentnature", "dn"],
    ["ltbapp_documenttype", "dt"],
    ["ltbapp_document", "doc"],
    ["ltbapp_record", "rec"],
    ["ltbapp_repository", "rep"],
    ["ltbapp_placename", "pn"],
    ["ltbapp_troupetype", "tt"],
    ["ltbapp_citationtype", "ct"],
    ["ltbapp_authortype", "at"],
    ["ltbapp_troupe", "tr"],
    ]
tableLookup = {}
for itm in tableData:
    tableLookup[itm[0]] = itm[1]
q = q.strip()

tbls = set()
def doTableSubs(itm):
    for tb in tableData:
        if re.search(tb[0], itm):
            tbls.add(tb[0])
            itm = re.sub(tb[0], tb[1],itm)
    return itm  

joins = re.findall(r"ON\s+([a-z0-9_.]+\s+=+\s+[a-z0-9_.]+)", q)
# print(joins)
j2 = []
for join in joins:
    j2.append(doTableSubs(join))
joinStr = " AND ".join(j2);
# print(joinStr)
selStr = doTableSubs(re.findall(r"(SELECT.*)\nFROM",q)[0])
# print(selStr)
ordStr = doTableSubs(re.findall(r"(ORDER BY.*)",q)[0])
# print(ordStr)
whereStr = "";
if re.search(r"WHERE",q):
    whereStr = re.findall(r"WHERE\s*(.*?)\s?ORDER",q)[0]
    whereStr = "AND "+doTableSubs(re.sub(r"[\)\(]","",whereStr))

fitem = []
for itm in tbls:
    fitem.append(itm+" AS "+tableLookup[itm])
fromStr = "FROM "+", ".join(fitem)
# print(fromStr)
q2p = [selStr,fromStr,"WHERE "+joinStr,ordStr]
if whereStr:
    q2p = [selStr,fromStr,"WHERE "+joinStr,whereStr,ordStr]
print("\n".join(q2p));
almostStr = '\t\t\t\t\t\t"'+'",\n\t\t\t\t\t\t"'.join(q2p)
print(almostStr[:-1]+'"\n')