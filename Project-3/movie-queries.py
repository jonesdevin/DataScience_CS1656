"""

@author: Devin Jones
@email: daj59@pitt.edu

"""

from neo4j import GraphDatabase, basic_auth

#connection with authentication
#driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "cs1656"), encrypted=False)

#connection without authentication
driver = GraphDatabase.driver("bolt://localhost:7687", encrypted=False)

session = driver.session()
transaction = session.begin_transaction()
f = open("output.txt", "w")


#1
f.write("### Q1 ###\n")
result = transaction.run('''MATCH (a:Actor)-[r]->(m:Movie)
 RETURN a.name, count(m) as movieCount
 order by movieCount desc limit 20''')
for record in result:
   f.writelines("{}, {}\n" .format(record['a.name'], record['movieCount']))
   
#2
f.write("\n### Q2 ###\n")
result = transaction.run('''MATCH (p:Person)-[r:RATED]->(m:Movie)
 WHERE r.stars <= 3
 RETURN m.title''')
for record in result:
   f.writelines("{}\n" .format(record['m.title']))
    
#3
f.write("\n### Q3 ###\n")
result = transaction.run('''MATCH (p:Person)-[r:RATED]->(m:Movie)<-[:ACTS_IN]-(a:Actor)
WITH m, count(a) as actors
RETURN m.title, actors
ORDER BY actors desc
LIMIT 1''')
for record in result:
   f.writelines("{}, {}\n" .format(record['m.title'], record['actors']))
       
   
#4
f.write("\n### Q4 ###\n")
result = transaction.run('''MATCH (a)-[r]->(m:Movie)<-[:DIRECTED]-(d:Director)
WITH a, count(distinct d) as dirs
WHERE dirs >= 3
RETURN a.name, dirs''')
for record in result:
   f.writelines("{}, {}\n" .format(record['a.name'], record['dirs']))
    
   
#5   
f.write("\n### Q5 ###\n")
result = transaction.run('''MATCH (kb:Actor{name:"Kevin Bacon"})-[:ACTS_IN]->(m1:Movie)<-[:ACTS_IN]-(a1:Actor)
WITH collect(a1.name) as oneBaconStrip
MATCH (a1:Actor)-[:ACTS_IN]->(m2:Movie)<-[:ACTS_IN]-(a2:Actor)
WHERE not a2.name in oneBaconStrip
RETURN distinct a2.name''' )
for record in result:
   f.writelines("{}\n" .format(record['a2.name']))
    

#6
f.write("\n### Q6 ###\n")
result = transaction.run('''MATCH (m:Movie)<-[:ACTS_IN]-(a:Actor{name: "Tom Hanks"})
RETURN distinct m.genre'''
   )
for record in result:
   f.writelines("{}\n" .format(record['m.genre']))
   
   
#7
f.write("\n### Q7 ###\n")
result = transaction.run('''MATCH (d:Director)-[:DIRECTED]->(m:Movie)
WITH distinct m.genre as num, d
WITH count(num) as nums, d
WHERE nums >=2
RETURN d.name, nums'''
   )
for record in result:
   f.writelines("{}, {}\n" .format(record['d.name'], record['nums']))
   
#8
f.write("\n### Q8 ###\n")
result = transaction.run('''Match (dir:Director)-[:DIRECTED]->(m:Movie)<-[:ACTS_IN]-(a:Actor)
Return dir.name, a.name, count(m)as counts
Order by count(m) desc
limit 5'''
   )
for record in result:
   f.writelines("{}, {}, {}\n" .format(record['dir.name'], record['a.name'], record['counts']))
   


f.close() 

transaction.close()
session.close()
