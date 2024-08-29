from click import option, group
from sideshow.utils.enums import generate_enum_typing_file
from mountaineer.cli import handle_runserver, handle_watch, handle_build
import django
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sideshow.settings")
django.setup()

@group()
def cli():
    pass

@cli.command()
@option("--port", default=5006, help="Port to run the server on")
def runserver(port: int):
    handle_runserver(
        package="sideshow",
        webservice="sideshow.app:app_controller.app",
        webcontroller="sideshow.app:app_controller",
        port=port,
    )


@cli.command()
def watch():
    handle_watch(
        package="sideshow",
        webcontroller="sideshow.app:app_controller",
    )


@cli.command()
def build():
    handle_build(
        webcontroller="sideshow.app:app_controller",
    )

@cli.command()
@option("--output-file", default="sideshow/views/src/enums.ts", help="Output file for the generated typing definitions")
def generate_enums(output_file: str):
    generate_enum_typing_file(output_file=output_file)

if __name__ == "__main__":
    cli()