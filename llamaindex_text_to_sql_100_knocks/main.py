from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, select, column

pgconfig = {
    'host': 'localhost',
    'port': 5432,
    'database': 'dsdojo_db',
    'user': 'padawan',
    'password': 'padawan12345',
}


def main():
    dsl = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        **pgconfig)
    engine = create_engine(dsl)
    # metadata_obj = MetaData(bind=engine)

    rs = engine.execute("SELECT 'このように実行できます' AS sample")
    for row in rs:
        print((row['sample']))


if __name__ == "__main__":
    main()
