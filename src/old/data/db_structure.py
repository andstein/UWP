### copied from wp20/lib/pwiki/wikidata/compact_sqlite

VERSION_DB = 8
VERSION_WRITECOMPAT = 8
VERSION_READCOMPAT = 8


# Helper for the following definitions
class t:
    pass
    
t.r = "real not null default 0.0"
t.i = "integer not null default 0"
t.pi = "integer primary key not null"
t.imo = "integer not null default -1"
t.t = "text not null default ''"
t.pt = "text primary key not null"
t.b = "blob not null default x''"



# Dictionary of definitions for all tables (as for changeTableSchema)
# Some of the tables are optional and don't have to be in the DB

TABLE_DEFINITIONS = {
    "changelog": (     # Essential if versioning used
        ("id", t.pi),
        ("word", t.t),
        ("op", t.i),
        ("content", t.b),
        ("compression", t.i),
        ("encryption", t.i),
        ("moddate", t.r)
        ),


    "headversion": (     # Essential if versioning used
        ("word", t.t),
        ("content", t.b),
        ("compression", t.i),
        ("encryption", t.i),
        ("modified", t.r),
        ("created", t.r)
        ),


    "versions": (     # Essential if versioning used
        ("id", t.pi),
        ("description", t.t),
        ("firstchangeid", t.i),
        ("created", t.r)
        ),


    "wikiwordcontent": (     # Essential
        ("word", t.t),
        ("content", t.b),
        ("compression", t.i),
        ("encryption", t.i),
        ("created", t.r),
        ("modified", t.r),
        ("visited", t.r),
        ("readonly", t.i),
        ("metadataprocessed", t.i),
        ("presentationdatablock", t.b),
        ),


    "wikirelations": (     # Cache
        ("word", t.t),
        ("relation", t.t),
        ("firstcharpos", t.imo)  # Position of the link from word to relation in chars
        ),


    "wikiwordprops": (     # Cache
        ("word", t.t),
        ("key", t.t),
        ("value", t.t),
        ("firstcharpos", t.imo)  # Position of the property in page in chars
        ),
    
    
    "todos": (     # Cache
        ("word", t.t),
        ("todo", t.t),
        ("firstcharpos", t.imo)  # Position of the todo in page in chars
        ),
        
    
    "search_views": (     # Deleted since 2.0alpha1. For updating format only 
        ("title", t.pt),
        ("datablock", t.b)
        ),
    
    
    "settings": (     # Essential since Compact 1.3
        ("key", t.pt),    # !!! primary key?
        ("value", t.t)
        ),

    "wikiwordmatchterms": (
        ("matchterm", t.t),
        ("matchtermnormcase", t.t),
        ("type", t.i),
        ("word", t.t),
        ("firstcharpos", t.imo)
        ),


    "datablocks": (
        ("unifiedname", t.t),
        ("data", t.b)
        )

# Not for compact:
#     "datablocksexternal": (
#         ("unifiedname", t.t),
#         ("filepath", t.t),
#         ("filenamelowercase", t.t),
#         ("filesignature", t.b)
#         )

    }


del t


MAIN_TABLES = (
    "wikiwordcontent",
    "wikirelations",
    "wikiwordprops",
    "todos",
#     "search_views",
    "settings",
    "wikiwordmatchterms",
    "datablocks"
    )
