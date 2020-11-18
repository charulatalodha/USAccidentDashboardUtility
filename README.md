Title : US Accident Reporting & Analysis Dashboard

• Created a shared MongoDB database cluster of 3 nodes on 3 EC2; each node configured as a 3-replica set for High Availability.

• Created multi key index; sharded 1M data; Map Reduce & Aggregation queries employed; Python menu driven application

# Tech Stack :
  Python (Pymongo), AWS EC2, Swap Memory, MongoDB (Sharding, Replication & Indexing)

  Data Size : 1 GB (3 million records)
  
# USAccidentDashboard
The U.S. Accident Analysis Dashboard is a utility tool that helps to store and understand trends in road
accidents drawn from the huge volume of data taken from 2016 to 2020. 

The project has a wide range of application use-cases to show potential results that can help authorities handle this overwhelmed situation by making critical decisions for improving public safety on roads. 

This application connects to MongoDB database designed to be highly available & consistent to users performing the queries.

It is a cluster of 3 nodes, a sharding system consisting of three shards, one mongos, and a replica set consisting of three config servers. For this application, due to huge volume of data in the database and the need to use map reduce and aggregate queries; therfore using MongoDB for enhanced performance is an optimal choice. 

The data set is supposed to be accessed and updated from many different sources such as the police department or insurance companies from different locations across the United States. Therefore, applying CAP theorem with high consistency and availability would be better for this scenario compared to ACID. The horizontal scalability will be able to facilitate the needs of this application.
