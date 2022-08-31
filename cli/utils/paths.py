from pathlib import Path

class ProjectTree:
    """ """

    def __init__(self, root):
        """ """
        if isinstance(root, ProjectTree):
            self._root = root.root
        else:
            self._root = Path(root)

    @property
    def root(self) -> Path:
        """ """
        return self._root

    @property
    def back(self) -> Path:
        """ """
        return self.root / "back"

    @property
    def back_src(self) -> Path:
        """ """
        return self.back / "src"

    @property
    def back_requirements(self) -> Path:
        """ """
        return self.back / "requirements.txt"

    @property
    def app_dist(self) -> Path:
        """ """
        return self.back_src / "static"

    @property
    def models(self) -> Path:
        """ """
        return self.back_src / "models"

    @property
    def venv(self) -> Path:
        """ """
        return self.back / "venv"

    @property
    def python(self):
        """ """
        return self.venv / "bin" / "python"

    @property
    def pip(self):
        """ """
        return self.venv / "bin" / "pip"

    @property
    def front(self) -> Path:
        """ """
        return self.root / "front"

    @property
    def front_env(self):
        """ """
        return self.front / ".env"
