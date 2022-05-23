import click
from app.clicommand.db_command import db
from app.clicommand.user_command import user


@click.group()
def cli():
    pass


cli.add_command(db)  # type: ignore
cli.add_command(user)  # type: ignore

if __name__ == '__main__':
    cli()
