#
# Database access functions for the web forum.
#

import time
import psycopg2
import bleach

## Database connection
#DB = []
#DB = psycopg2.connect("dbname=forum")

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    #posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    #posts.sort(key=lambda row: row['time'], reverse=True)
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    query = "SELECT time, content FROM posts order by time DESC;"
    c.execute(query)
    posts = ({'content' : str(row[1]), 'time' : str(row[0])} for row in c.fetchall())
    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    #t = time.strftime('%c', time.localtime())
    #DB.append((t, content))
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    #c.execute( "INSERT INTO posts (content) VALUES ('%s')" % content )
    # ^^^ above is an unsafe way (string parameter interpolation), never do it.
    # SQL injection attack query , such as  '); delte from posts;--
    cont = bleach.clean(content)    # clean up unsafe insert content (such as javascript attach)
    c.execute( "INSERT INTO posts (content) VALUES (%s)", (cont,) )
    DB.commit()
    DB.close()


# use update to remove bad content already in DB
# "UPDATE posts set content='chesse' where content like '%spam%';"

# also cna delete dummy content
# DELETE from posts where content='cheese';

