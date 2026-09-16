Think about this as you run these multiple servers 

Answer these questions through observation and discussion:

# Question 1

Are we running three physical computers?

# Question 2

If all three servers are running on one computer, why do they need different ports?

# Question 3

What happens when Server 2 stops?

# Question 4

Can the client still communicate with Servers 1 and 3?

# Question 5

Should the client continue trying to contact Server 2?

# Question 6

If we had 1,000 clients, would it be convenient for every client to know the location and status of every server?


# experiment
1. SERVER failure
2. slow server (The /slow endpoint intentionally takes several seconds to respond.)

# Next lab
In the next lab, we will introduce a Load Balancer, The load balancer will decide which server should receive each request.