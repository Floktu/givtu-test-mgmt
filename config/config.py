## Config for connecting to db
db_config = {
    'dev':
        {
            'user': 'admin',
            'password': 'terraformdb123',
            'host': 'givtu-dev-sydney-database.coyeaggqwolq.ap-southeast-2.rds.amazonaws.com',
            'port': 3306,
            'database': 'givtudevsydney',
            'raise_on_warnings': False,
        },
    'staging':
        {
            'user': 'admin',
            'password': 'terraformdb123',
            'host': 'givtu-stage-sydney-database.coyeaggqwolq.ap-southeast-2.rds.amazonaws.com',
            'port': 3306,
            'database': 'givtudevsydney',
            'raise_on_warnings': False,
        },
    'gamedev':
        {
            'user': 'admin',
            'password': 'terraformdb123',
            'host': 'givtudevsydney-1.coyeaggqwolq.ap-southeast-2.rds.amazonaws.com',
            'port': 3306,
            'database': 'givtudevsydney',
            'raise_on_warnings': False,
        },
    'local':
        {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'port': 3306,
            'database': 'givtudevsydney',
            'raise_on_warnings': False,
        },
    'prod2':
        {
            # 'user': 'admin',
            # 'password': 'mmErtMZ23i5wNSKP3dtwh',
            # 'host': 'givtuprod-1.c3smuaik4oeg.ap-southeast-2.rds.amazonaws.com',
            # 'port': 3306,
            # 'database': 'givtuprod',
            # 'raise_on_warnings': False,
        }
}

api_config = {
    'local': 'http://localhost:8741',
    'staging': 'https://staging.givtu.com',
    'gamedev': 'https://gamedev.givtu.com',
    'dev': 'https://givtu-dev-sydney.givtu.com'
}
