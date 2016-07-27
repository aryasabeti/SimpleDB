# SimpleDB

A Python 3 solution to the [Simple Database Challenge]


##### Usage
Interactive: `python3 simpledb.py`

With commands from file, 1 per line: `python3 simpledb.py < commands.txt`


##### Tests
SimpleDB uses pytest.
```
cd SimpleDB
./runtest.sh
```


##### Performance
Database updates (`get`, `set`, `unset`) as well as reference counting (`numequalto`) perform in `O(1)` time since these methods only read or modify a single value in each of a finite number of dictionaries. `get` and `set` may also append to a list in order to store transaction history, also in `O(1)`.

`O(M)` memory will be used for each open transaction, where M is the number of values modified in the given transaction.


##### Possible Improvements
* `get` and `set` are misleading names since they also perform bookkeeping for transactions and reference counting. Extracting this logic using decorators or similar would improve readability and clarity.
* Using print statements produces correct output in the simplest way, but the API could be cleanly separated from the UI, by adding an additional layer of indirection in `db_adapter` which translates user input to SimpleDB commands. This would also allow choice of a different grammar for user commands.

[Simple Database Challenge]: <https://www.thumbtack.com/challenges/simple-database>
