##############################################################################################
# List all tasks
# curl -i http://localhost:5000/todo/api/v1.0/tasks/all

# List open tasks
# curl -i http://localhost:5000/todo/api/v1.0/tasks

# List types
# curl -i http://localhost:5000/todo/api/v1.0/types

# read a task
# curl -i http://localhost:5000/todo/api/v1.0/tasks/2

# read a task
# curl -i http://localhost:5000/todo/api/v1.0/tasks/computer'

# add a task
# curl -i  -X POST -d "{\"item\":\"Read a book\", \"type\":\"computer\"}" -H "Content-Type: application/json" http://localhost:5000/todo/api/v1.0/tasks

# Update a task
#  curl -i -X PUT -d "{\"done\":true}" -H "Content-Type: application/json" http://localhost:5000/todo/api/v1.0/tasks/2

# curl -i -X PUT -d  "{ \"item\":\"Go to bed early\", \"status\":\"closed\"}" -H "Content-Type: application/json" http://localhost:5000/todo/api/v1.0/tasks/562

# delete a task
# curl -i -X DELETE http://localhost:5000/todo/api/v1.0/tasks/2

##############################################################################################