(function() {
  var i, text, code, codes = document.getElementsByTagName('code');
  for (i = 0; i < codes.length;) {
    code = codes[i];
    if (code.parentNode.tagName !== 'PRE' && code.childElementCount === 0) {
      text = code.textContent;
      if (/^\$[^$]/.test(text) && /[^$]\$$/.test(text)) {
        text = text.replace(/^\$/, '\\(').replace(/\$$/, '\\)');
        code.textContent = text;
      }
      if (/^\\\((.|\s)+\\\)$/.test(text) || /^\\\[(.|\s)+\\\]$/.test(text) ||
          /^\$(.|\s)+\$$/.test(text) ||
          /^\\begin\{([^}]+)\}(.|\s)+\\end\{[^}]+\}$/.test(text)) {
        code.outerHTML = code.innerHTML;  // remove <code></code>
        continue;
      }
    }
    i++;
  }
})();

<script src="//yihui.name/js/math-code.js"></script>
<!-- Just one possible MathJax CDN below. You may use others. -->
<script async
  src="//mathjax.rstudio.com/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

# grouppayment
You go out with a group of friends, and everyone covers a different purchase with a deposit. How do you Venmo each other back? You could split each deposit by `$n$` and make `$2*frac{(n*(n+1),2}$` transactions. Or you could simplify the number of transactions into something like $O(n)$.

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
Working...
SIMPLIFIED GRAPH
[&apos;Akash&apos;, &apos;Bob&apos;, &apos;Cixun&apos;, &apos;David&apos;, &apos;Esther&apos;]
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
</pre>



#### Verification:

Verification is simple. If you make a graph of who owes whom what after splitting the deposits, the total flow in and out of a node should be the same before and after running the simplification process. In other words, everyone ends up with the same net payment.

