# CodeFoo2019

The written answers to the witcher questions are at the end of witcher_proj.py.

To run the chat application:

1) Run server.py
2) Run 2 instances of client.py
3) enter the same hostname in the 2 client.py instances

MORE ABOUT THE CHAT APP:

The server not only passes messages back and forth between clients,
but after the chat is finished, it stores the messages in a SQL database.
The idea was that whenever two people have communicated via this app in the past,
if they enter their previous usernames, the clients will
perform a query for messages with the their usernames matching those 
of the sender and recipient, sort them by timestamp, and display
them in the chat window.

I'm going to work on this project in the future, if only as a hobby,
and add this, as well as a gui.

