from pathlib import Path

class ProjectTree:
    """ """

    def __init__(self, root):
        """ """
        if isinstance(root, ProjectTree):
            self._root = root.root
        else:
            self._root = Path(root)

    def __repr__(self):
        """ """
        return repr(self.root)

    def __str__(self):
        """ """
        return str(self.root)

    @property
    def root(self):
        return self._root

    @property
    def venv(self):
        return self.root / "venv"
    @property
    def python(self):
        return self.venv / "bin" / "python"
    @property
    def pip(self):
        return self.venv / "bin" / "pip"

    @property
    def src(self):
        return self.root / "src"

    @property
    def requirements(self):
        return self.root / "requirements.txt"

    @property
    def front(self):
        return self.src / "front"
    @property
    def front_env(self):
        return self.front / ".env"

    @property
    def ml(self):
        return self.src / "ml"
    @property
    def processed_data(self):
        return self.ml / "data" / "processed"
    @property
    def unprocessed_data(self):
        return self.ml / "data" / "processed"


    @property
    def server(self):
        return self.src / "server"
    @property
    def flask_app(self):
        return self.server / "app.py"
    @property
    def app_dist(self):
        return self.server / "static"
    @property
    def saved_models(self):
        return self.server / "saved_models"
