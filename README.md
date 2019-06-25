# grouppayment
Simplifying splitting the bills among a group

Still in production phase so send all the bugs! Also, narrow usage goals so not cosmically robust


#### Usage:

python groupPayment.py --names Akash Bob Cixun David Esther --deposits 100 150.5 40.66 300 300
['Akash', 'Bob', 'Cixun', 'David', 'Esther']
[100.0, 150.5, 40.66, 300.0, 300.0]
ORIGINAL UNIDIRECTIONAL GRAPH
['Akash', 'Bob', 'Cixun', 'David', 'Esther']
[[   nan 10.1    0.    40.    40.   ]
 [ 0.       nan  0.    29.9   29.9  ]
 [11.868 21.968    nan 51.868 51.868]
 [ 0.     0.     0.       nan  0.   ]
 [ 0.     0.     0.     0.       nan]]
Working...
SIMPLIFIED GRAPH
['Akash', 'Bob', 'Cixun', 'David', 'Esther']
[[   nan  0.     0.    38.232 40.   ]
 [ 0.       nan  0.     0.    29.9  ]
 [ 0.     0.       nan 85.704 51.868]
 [ 0.     2.168  0.       nan  0.   ]
 [ 0.     0.     0.     0.       nan]]


Akash gives David 38.232
Akash gives Esther 40.0
Bob gives Esther 29.9
Cixun gives David 85.70400000000001
Cixun gives Esther 51.868
David gives Bob 2.1680000000000064





----- done -----


#### Verification:

Verification is simple. If you make a graph of who owes whom what after splitting the deposits, the total flow in and out of a node should be the same before and after running the simplification process. In other words, everyone ends up with the same net payment.

