from collections import defaultdict
from sys import exit, stdin


class SimpleDB:
    def __init__(self):
        self._data = {}
        self._refcounts = defaultdict(lambda: 0)
        self._transactions = []

    def set(self, name, value):
        self._record_if_transaction(name)
        self._refcounts[value] += 1
        self._data[name] = value
        return True

    def get(self, name):
        value = self._data.get(name, None)
        print(value if value else 'NULL')
        return value

    def unset(self, name):
        self._record_if_transaction(name)
        value = self._data.pop(name, None)
        if value:
            self._refcounts[value] -= 1
        return value

    def numequalto(self, value):
        refcount = self._refcounts[value]
        print(refcount)
        return refcount

    def _record_if_transaction(self, name):
        if self._transactions:
            latest = self._transactions[-1]
            if name not in latest:
                if name in self._data:
                    latest[name] = self._data[name]
                else:
                    latest[name] = None

    def begin(self):
        self._transactions.append({})

    def commit(self):
        if self._transactions:
            self._transactions = []
            return True
        else:
            print('NO TRANSACTION')
            return False

    def rollback(self):
        if self._transactions:
            latest = self._transactions[-1]
            for name, value in latest.items():
                if value:
                    self.set(name, value)
                else:
                    self.unset(name)
            self._transactions.pop()
            return True
        else:
            print('NO TRANSACTION')
            return False


def db_adapter(from_stdin, db):
    from_stdin = from_stdin.strip()

    if from_stdin:
        from_stdin = from_stdin.split()
        command, args = from_stdin[0].lower(), from_stdin[1:]

        if command == 'end':
            exit()

        try:
            db_method = getattr(db, command)
            db_method(*args)
        except:
            print("Could not issue command")


if __name__ == '__main__':
    db = SimpleDB()
    for line in stdin:
        db_adapter(line, db)
