from django.db.models.sql import compiler

class SQLCompiler(compiler.SQLCompiler):
    pass

class SQLInsertCompiler(compiler.SQLInsertCompiler):
    def execute_sql(self, return_id=False):
        self.return_id = return_id
        cursor = super(compiler.SQLInsertCompiler, self).execute_sql(None)
        if not (return_id and cursor):
            return
        if self.connection.features.can_return_id_from_insert:
            return self.connection.ops.fetch_returned_insert_id(cursor)
        if 'db_seq' in self.query.model._meta.__dict__:
            return self.connection.ops.last_insert_id(cursor,
                self.query.model._meta.db_seq, '')
        else:
            return self.connection.ops.last_insert_id(cursor,
                self.query.model._meta.db_table, self.query.model._meta.pk.column)

class SQLDeleteCompiler(compiler.SQLDeleteCompiler):
    pass

class SQLUpdateCompiler(compiler.SQLUpdateCompiler):
    pass

class SQLAggregateCompiler(compiler.SQLAggregateCompiler):
    pass

class SQLDateCompiler(compiler.SQLDateCompiler):
    pass
