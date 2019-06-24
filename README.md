# grouppayment
Simplifying splitting the bills among a group

Still in production phase so send all the bugs! Also, narrow usage goals so not cosmically robust


#### Usage:

python groupPayment.py --names Akash Bob Cixun David Esther --deposits 100 150.5 40.66 300 300


#### Verification:

Verification is simple. If you make a graph of who owes whom what after splitting the deposits, the total flow in and out of a node should be the same before and after running the simplification process. In other words, everyone ends up with the same net payment.

