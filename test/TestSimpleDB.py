from simpledb import SimpleDB


class TestSimpleDB:

    def setup(self):
        self.db = SimpleDB()

    def test_set_new(self):
        assert self.db.set('name', 1) is True

    def test_set_updates_existing(self):
        assert self.db.set('name', 1) is True
        assert self.db.set('name', 2) is True
        assert self.db.get('name') == 2

    def test_get_existing(self):
        self.db.set('name', 1)
        assert self.db.get('name') == 1

    def test_get_existing_repeatedly(self):
        self.db.set('name', 1)
        assert self.db.get('name') == 1
        assert self.db.get('name') == 1

    def test_get_nonexisting(self):
        assert self.db.get('nonexisting') is None

    def test_unset_existing(self):
        self.db.set('name', 1)
        assert self.db.unset('name') == 1

    def test_unset_existing_repeatedly(self):
        self.db.set('name', 1)
        assert self.db.unset('name') == 1
        assert self.db.unset('name') is None

    def test_unset_nonexisting(self):
        assert self.db.unset('nonexisting') is None

    def test_numequalto_default(self):
        assert self.db.numequalto(1) == 0

    def test_numequalto_refcount(self):
        self.db.set('name', 123)
        assert self.db.numequalto(123) == 1
        self.db.set('othername', 123)
        assert self.db.numequalto(123) == 2

        self.db.unset('name')
        assert self.db.numequalto(123) == 1
        self.db.unset('othername')
        assert self.db.numequalto(123) == 0

    def test_numequal_nonexisting(self):
        assert self.db.numequalto(1) == 0

    def test_transaction(self):
        self.db.begin()
        self.db.set('name', 1)
        self.db.commit()
        assert self.db.get('name') == 1

    def test_rollback(self):
        self.db.begin()
        self.db.set('name', 1)
        self.db.rollback()
        assert self.db.get('name') is None

    # Given test cases below

    def test_rollback_many(self):
        self.db.begin()
        self.db.set('a', 10)
        assert self.db.get('a') == 10

        self.db.begin()
        self.db.set('a', 20)
        assert self.db.get('a') == 20

        self.db.rollback()
        assert self.db.get('a') == 10

        self.db.rollback()
        assert self.db.get('a') is None

    def test_rollback_and_commit_nonexisting(self):
        self.db.begin()
        self.db.set('a', 30)

        self.db.begin()
        self.db.set('a', 40)

        self.db.commit()

        assert self.db.get('a') == 40
        assert self.db.rollback() is False
        assert self.db.commit() is False

    def test_rollback_and_commit_with_unset(self):
        self.db.set('a', 50)
        self.db.begin()
        assert self.db.get('a') == 50

        self.db.set('a', 60)
        self.db.begin()
        self.db.unset('a')
        assert self.db.get('a') is None

        self.db.rollback()
        assert self.db.get('a') == 60

        self.db.commit()
        assert self.db.get('a') == 60

    def test_rollback_and_commit_refcounts(self):
        self.db.set('a', 10)
        self.db.begin()
        assert self.db.numequalto(10) == 1

        self.db.begin()
        self.db.unset('a')
        assert self.db.numequalto(10) == 0

        self.db.rollback()
        assert self.db.numequalto(10) == 1
