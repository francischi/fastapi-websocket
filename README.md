# redis + fastapi + websocket :zap::zap:

**T**his is an example to show how to use websocket throught redis.
The original way to use websocket in fastapi official document is **nice** to use when the project is small,
but when it comes to a bigger project, you will add some cache policy into project such as 'redis', 
or some load balance policy such as 'uvicorn workers','nginx load balancer',then you will have to make some effort on how to combine your application with those policies.

**T**his project provide a more **efficient、scalable** way to let you use websocket combine with redis.

**T**here are some benefits using redis as a pubsub service
* extensibility
* fast
* wont be limit by programming language
* normal ( its popular to use redis as a cache service )

### How to use it
* cd in this project
  
**run redis service** ```(if you have redis already u can skip this step)```
* ```
  ./redis/redis-server.exe
**use pipenv run  main.py**
* ```
  pipenv shell
* ```
  pipenv install
* ```
  pipenv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
  ```
**socket.html**
* ```
  if you use xampp to run your database and phpmyadmin, ypu can put socket.html
  in path below:

    C:\xampp\htdocs\socket.html
  
  type localhost/socket.html as URL and enjoy it !!!
  ```

### *notice
make sure your redis serve on port 6379
make sure your frontend code is something like below ("ws://127.0.0.1:8000/ws/user1")
~~~
<script>
    var ws = new WebSocket("ws://127.0.0.1:8000/ws/user1");

    ws.onmessage = function(event) {
        var messages = document.getElementById('messages')
        var message = document.createElement('li')
        var content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
    };
    function sendMessage(event) {
        var input = document.getElementById("messageText")
        ws.send(input.value)
        input.value = ''
        event.preventDefault()
    }
</script>
