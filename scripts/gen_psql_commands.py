command = \
"""
sudo -u postgres psql

create user {db_user} with encrypted password '{db_pass}';
create database {db_name} with encoding 'utf8' owner {db_user};
\q
"""

def main():
    db_name = input('db_name: ')
    db_user = input('db_user: ')
    db_pass = input('db_pass: ')

    result_command = command.format(
        db_name=db_name,
        db_user=db_user,
        db_pass=db_pass
    )
    print("-"*75)
    print(result_command)
    print("-"*75)


if __name__ == '__main__':
    main()


