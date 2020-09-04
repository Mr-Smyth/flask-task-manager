# To create a search index:

### From within the python terminal:

* from app import mongo
* mongo.db.tasks.create_index([("task_name", "text"), ("task_description", "text")])

### Show the details of the search index:

* mongo.db.tasks.index_information()

### To drop a search index:

* mongo.db.tasks.drop_index('task_name_text_task_description_text')
    * remember to specify the name in brackets

 ### Drop all search Indexes:

 * mongo.db.tasks.drop_indexes()


# To exit:

* quit()