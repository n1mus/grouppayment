# grouppayment
You go out with a group of friends, and everyone covers a different purchase with a deposit. How do you Venmo each other back? You could split each deposit by `n` and make `2*(n*(n+1)/2)` transactions. Or you could simplify the number of transactions into something like `O(n)` (?).

Still in production phase so send all the bugs! Also, narrow usage goals so not cosmically robust


#### Usage:

<pre>
python groupPayment.py --names Akash Bob Cixun David Esther --deposits 100 150.5 40.66 300 300
[&apos;Akash&apos;, &apos;Bob&apos;, &apos;Cixun&apos;, &apos;David&apos;, &apos;Esther&apos;]
[100.0, 150.5, 40.66, 300.0, 300.0]
ORIGINAL UNIDIRECTIONAL GRAPH
[&apos;Akash&apos;, &apos;Bob&apos;, &apos;Cixun&apos;, &apos;David&apos;, &apos;Esther&apos;]
[[   nan 10.1    0.    40.    40.   ]
 [ 0.       nan  0.    29.9   29.9  ]
 [11.868 21.968    nan 51.868 51.868]
 [ 0.     0.     0.       nan  0.   ]
 [ 0.     0.     0.     0.       nan]]
Iterating........
SIMPLIFIED GRAPH
[&apos;Akash&apos;, &apos;Bob&apos;, &apos;Cixun&apos;, &apos;David&apos;, &apos;Esther&apos;]
[[    nan   0.      0.      0.     78.232]
 [  0.        nan   0.      0.     27.732]
 [  0.      0.        nan 137.572   0.   ]
 [  0.      0.      0.        nan  15.804]
 [  0.      0.      0.      0.        nan]]


Akash gives Esther 78.232
Bob gives Esther 27.731999999999992
Cixun gives David 137.572
David gives Esther 15.80400000000001





----- done -----
</pre>



#### Verification:

Verification is simple. If you make a graph of who owes whom what after splitting the deposits, the total flow in and out of a node should be the same before and after running the simplification process. In other words, everyone ends up with the same net payment.

