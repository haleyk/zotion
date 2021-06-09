from notion_client import Client
from pyzotero import zotero

def get_authors(creator_list):
    authors = ''
    for c in creator_list:
        if c['creatorType'] == 'author':
            nm = c['firstName'] + ' ' + c['lastName']
            if len(authors) != 0:
                nm = ', '+nm
            authors += nm
    return authors

def year_parse(yearstr):
    if len(yearstr) == 4:
        return yearstr
    splits = ['/', '-']
    for s in splits:
        if s in yearstr:
            all_dates = yearstr.split(s)
            yr_guess = [x for x in all_dates if len(x)==4][0]
            return yr_guess
    return yearstr

# library_type will be 'user' if it's you
zot = zotero.Zotero(library_id, library_type, api_key)
notion = Client(auth='your client')
zotero_database = zot.collection_items_top(database_id)
for item in zotero_database:
    try:
        title = item['data']['title']
        year = year_parse(item['data']['date'])
        auth = get_authors(item['data']['creators'])
        authdict = {"type": "rich_text", "rich_text": [{"type": "text", "text": {"content": auth},},],}
        yrdict = {"type": "rich_text", "rich_text": [{"type": "text", "text": {"content": year},},],}
        prop = {"Name": {"title": [{"text": {"content": title}}]}, "Authors": authdict, "Year": yrdict}
        # make sure your notion database has author and year pieces!
        n = notion.pages.create(parent={"database_id": your_database_id}, properties=prop)
    except:
        print(item['data'])

# eof
