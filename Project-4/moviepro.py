import sqlite3 as lite
import csv
import re
con = lite.connect('cs1656.sqlite')

with con:
    cur = con.cursor() 

    ########################################################################        
    ### CREATE TABLES ######################################################
    ########################################################################        
    # DO NOT MODIFY - START 
    cur.execute('DROP TABLE IF EXISTS Actors')
    cur.execute("CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

    cur.execute('DROP TABLE IF EXISTS Movies')
    cur.execute("CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

    cur.execute('DROP TABLE IF EXISTS Directors')
    cur.execute("CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

    cur.execute('DROP TABLE IF EXISTS Cast')
    cur.execute("CREATE TABLE Cast(aid INT, mid INT, role TEXT)")

    cur.execute('DROP TABLE IF EXISTS Movie_Director')
    cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")
    # DO NOT MODIFY - END

    ########################################################################        
    ### READ DATA FROM FILES ###############################################
    ########################################################################        
    # actors.csv, cast.csv, directors.csv, movie_dir.csv, movies.csv
    # UPDATE THIS
    
    #Actors (aid, fname, lname, gender)
    with open('actors.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            cur.execute("INSERT INTO Actors VALUES({}, '{}', '{}', '{}')" .format(row[0], row[1], row[2], row[3])) 
    
    #Movies (mid, title, year, rank)
    with open('movies.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            cur.execute("INSERT INTO Movies VALUES({}, '{}', {}, {})" .format(row[0], row[1], row[2], row[3])) 


    #Directors (did, fname, lname)
    with open('directors.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            cur.execute("INSERT INTO Directors VALUES({}, '{}', '{}')" .format(row[0], row[1], row[2])) 

    #Cast (aid, mid, role)
    with open('cast.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            cur.execute("INSERT INTO Cast VALUES({}, {}, '{}')" .format(row[0], row[1], row[2]))  

    #Movie_Director (did, mid)
    with open('movie_dir.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for row in csv_reader:
            cur.execute("INSERT INTO Movie_Director VALUES({}, {})" .format(row[0], row[1])) 



    ########################################################################        
    ### INSERT DATA INTO DATABASE ##########################################
    ########################################################################        
    # UPDATE THIS TO WORK WITH DATA READ IN FROM CSV FILES
    #cur.execute("INSERT INTO Actors VALUES(1001, 'Harrison', 'Ford', 'Male')") 
    #cur.execute("INSERT INTO Actors VALUES(1003, 'Day', 'Ridley', 'Female')")
    #cur.execute("INSERT INTO Actors VALUES(1004, 'Say', 'Rooney', 'Female')")  
    #cur.execute("INSERT INTO Actors VALUES(1006, 'Tom', 'Hanks', 'Male')")  

    #cur.execute("INSERT INTO Movies VALUES(101, 'Star Wars VII: The Force Awakens', 2015, 8.2)") 
    #cur.execute("INSERT INTO Movies VALUES(103, 'ARogue One: A Star Wars Story', 2016, 2.0)")
    
    #cur.execute("INSERT INTO Cast VALUES(1006, 102, 'Solo')")  
    #cur.execute("INSERT INTO Cast VALUES(1004, 102, 'Reyss')") 
    #cur.execute("INSERT INTO Cast VALUES(1001, 102, 'Reyd')") 
    #cur.execute("INSERT INTO Cast VALUES(1001, 103, 'Reys')") 

    #cur.execute("INSERT INTO Directors VALUES(5002, 'Harold', 'Ford')")  
    #cur.execute("INSERT INTO Directors VALUES(5003, 'Harold', 'Ridley')")  
    
    
    #cur.execute("INSERT INTO Movie_Director VALUES(5002, 101)")  
    #cur.execute("INSERT INTO Movie_Director VALUES(5003, 102)") 

    con.commit()
    
        

    ########################################################################        
    ### QUERY SECTION ######################################################
    ########################################################################        
    queries = {}

    # DO NOT MODIFY - START     
    # DEBUG: all_movies ########################
    queries['all_movies'] = '''
SELECT * FROM Movies
'''    
    # DEBUG: all_actors ########################
    queries['all_actors'] = '''
SELECT * FROM Actors
'''    
    # DEBUG: all_cast ########################
    queries['all_cast'] = '''
SELECT * FROM Cast
'''    
    # DEBUG: all_directors ########################
    queries['all_directors'] = '''
SELECT * FROM Directors
'''    
    # DEBUG: all_movie_dir ########################
    queries['all_movie_dir'] = '''
SELECT * FROM Movie_Director
'''    
    # DO NOT MODIFY - END

    ########################################################################        
    ### INSERT YOUR QUERIES HERE ###########################################
    ########################################################################        
    # NOTE: You are allowed to also include other queries here (e.g., 
    # for creating views), that will be executed in alphabetical order.
    # We will grade your program based on the output files q01.csv, 
    # q02.csv, ..., q12.csv


    #CORRECT
    # Q01 - List all the actors (first and last name) who acted in at least one film in the 90s 
    #       (1990-1999, both ends inclusive) and in at least one film after 2009.
    #       Sort all actor names alphabetically (last name, first name). 
    ########################        
    queries['q01'] = '''SELECT  fname, lname 
    FROM (Actors natural join (SELECT distinct aid FROM Movies natural join Cast WHERE year > 2009)) natural join (SELECT distinct aid FROM Movies natural join Cast WHERE year between 1990 and 1999)
    ORDER BY lname, fname asc
'''    
    #CORRECT
    # Q02 ######################## '''
    '''List all the movies (title, year) that were released in the same year as the movie 
        entitled "Star Wars VII: The Force Awakens", but had a better rank than it 
        (Note: the higher the value in the rank attribute, the better the rank of the movie). 
        Sort alphabetically by movie title.
    '''        
    queries['q02'] = '''SELECT title, year
    FROM Movies natural join(SELECT year from Movies WHERE title = 'Star Wars VII: The Force Awakens')
    WHERE rank > (SELECT rank from Movies WHERE title = 'Star Wars VII: The Force Awakens')
    ORDER BY title asc
'''    
    #CORRECT
    # Q03 ########################
    '''List all the actors (first and last name) who played in a Star Wars movie 
        (i.e., title like '%Star Wars%') in decreasing order of how many Star Wars movies they
        appeared in. If an actor plays multiple roles in the same movie, 
        count that still as one movie.
    '''      
    queries['q03'] = '''SELECT fname, lname
    FROM Actors natural join (SELECT aid, mid 
                              FROM CAST natural join Movies WHERE title like '%Star Wars%')
    Group by fname, lname
    Order by count(distinct mid) desc
'''    
    #CORRECT
    # Q04 ######################## 
    '''Find the actor(s) (first and last name) who ONLY acted in films released before 1987. 
    Sort all actor names alphabetically (last name, first name).  
'''     
    queries['q04'] = '''SELECT fname, lname
        FROM Actors natural join(SELECT aid
        FROM (SELECT aid FROM Movies natural join Cast WHERE year < 1987)
        
        EXCEPT 
        
        SELECT aid
        FROM (SELECT aid FROM Movies natural join Cast WHERE year > 1986))
    ORDER BY lname, fname asc
'''    
    #CORRECT
    # Q05 ########################   
    ''' List the top 20 directors in descending order of the number of films they directed
        (first name, last name, number of films directed). For simplicity,
        feel free to ignore ties at the number 20 spot (i.e., always show up to 20 only).
'''     
    queries['q05'] = '''SELECT fname, lname, count(mid)
    FROM Directors natural join Movie_Director
    Group by fname, lname
    Order by count(mid) desc
    LIMIT 20
'''    
    #CORRECT
    # Q06 ########################  
    '''Find the top 20 movies with the largest cast (title, number of cast members)
        in decreasing order. Note: show all movies in case of a tie for the 20th spot.
'''      
    queries['q06'] = '''SELECT title, count(aid) as counts
    FROM Cast natural join Movies    
    Group by title
    Having counts in (SELECT distinct counts 
         FROM(SELECT title, count(aid) as counts
              FROM Cast natural join Movies
              Group by title
        Order by count(aid) desc) LIMIT 20)
    Order by count(aid) desc 
'''    
    

    #CORRECT
    # Q07 ######################## 
    '''Find the movie(s) whose cast has more actresses than actors 
    (i.e., gender=female vs gender=male). Show the movie title, the number of actresses, 
    and the number of actors in the results. Sort alphabetically by movie title
'''       

    queries['q07'] = '''SELECT title, CountF, (select coalesce(CountM, 0))
    FROM Movies Natural join ((SELECT mid, count(aid) as CountF FROM Cast natural join Actors
         WHERE UPPER(gender) = UPPER('female')  Group by mid)a left outer join (SELECT mid, count(aid) as CountM FROM Cast natural join Actors
         WHERE UPPER(gender) = UPPER('male')  Group by mid)b on a.mid=b.mid)  
    WHERE CountF > (select coalesce(CountM, 0))
    Order By title asc
'''    
    #CORRECT
    # Q08 ########################   
    '''Find all the actors who have worked with at least 6 different directors. 
    Do not consider cases of self-directing (i.e., when the director is also an actor in a movie),
    but count all directors in a movie towards the threshold of 6 directors. Show the actor's 
    first, last name, and the number of directors he/she has worked with.
    Sort in decreasing order of number of directors.
'''     
    queries['q08'] = '''SELECT a.fname, a.lname, count(distinct did) as numDir
    FROM Actors as a join ((Movie_Director natural join Directors )natural join Cast)as m on a.aid = m.aid
    WHERE (a.fname != m.fname) AND (a.lname != m.lname)
    Group by a.aid
    Having numDir >= 6
    Order by count(distinct did) desc
    
'''    
    #CORRECT
    # Q09 ########################        
    queries['q09'] = '''SELECT fname, lname, count(mid) as counts
    FROM (Movies natural join Cast) natural join((Actors)natural join(SELECT  a.aid, min(year) as year
        FROM (SELECT * FROM Actors Where UPPER(fname) like 'S%')a natural join (cast natural join Movies)
        Group by fname, lname))t
    group by t.aid
    order by counts desc
    
'''    



    #CORRECT
    # Q10 ########################        
    queries['q10'] = '''Select t.lname, title
    FROM Movies Natural join((Actors natural join(cast))a join 
                             (Movie_Director natural join Directors)m on a.lname = m.lname AND a.mid=m.mid)t
    Order by t.lname asc
'''    
    #CORRECT
    # Q11 ########################        
    queries['q11'] = '''
        SELECT fname, lname
        FROM (CAST natural join Actors) natural join
    
            (SELECT mid
            FROM Cast natural join
                (SELECT distinct b.aid
                 FROM Cast a join
                     (SELECT f.aid, f.mid, fname, lname
                      FROM (Cast natural join Actors)f join (Cast natural Join(Select aid from actors where fname = 'Tom' and lname = 'Hanks'))v on f.mid = v.mid 
                WHERE fname != 'Tom' AND lname != 'Hanks')b on a.mid = b.mid)
            Except
            
            SELECT mid
            FROM (CAST natural join (Select aid from actors where fname = 'Tom' and lname = 'Hanks')))

        EXCEPT
    
            SELECT b.fname, b.lname
            FROM Cast a join
            (SELECT f.aid, f.mid, fname, lname
            FROM (Cast natural join Actors)f join (Cast natural Join(Select aid from actors where fname = 'Tom' and lname = 'Hanks'))v on f.mid = v.mid 
            WHERE fname != 'Tom' AND lname != 'Hanks')b on a.mid = b.mid
        
        ORDER BY lname, fname
'''    
    #CORRECT
    # Q12 ########################        
    queries['q12'] = '''SELECT fname, lname, counts, popularity
        FROM Actors natural join
        (SELECT aid, count(mid) as counts, avg(rank)as popularity
         FROM CAST natural join Movies
         Group by aid
         ORDER by popularity desc
         LIMIT 20)
'''    



    ########################################################################        
    ### SAVE RESULTS TO FILES ##############################################
    ########################################################################        
    # DO NOT MODIFY - START     
    for (qkey, qstring) in sorted(queries.items()):
        try:
            cur.execute(qstring)
            all_rows = cur.fetchall()
            
            print ("=========== ",qkey," QUERY ======================")
            print (qstring)
            print ("----------- ",qkey," RESULTS --------------------")
            for row in all_rows:
                print (row)
            print (" ")

            save_to_file = (re.search(r'q0\d', qkey) or re.search(r'q1[012]', qkey))
            if (save_to_file):
                with open(qkey+'.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(all_rows)
                    f.close()
                print ("----------- ",qkey+".csv"," *SAVED* ----------------\n")
        
        except lite.Error as e:
            print ("An error occurred:", e.args[0])
    # DO NOT MODIFY - END
    
