import yaml

with open("config.yaml", encoding="UTF-8") as file:
    CONFIG_YAML = yaml.safe_load(file)

class YAMLParser(type):
    subsection = None

    def __getattr__(self, name):
        name = name.lower()

        try:
            if self.subsection is not None:
                return CONFIG_YAML[self.section][self.subsection][name]
            return CONFIG_YAML[self.section][name]
        except KeyError as e:
            dotted_path = '.'.join(
                (self.section, self.subsection, name)
                if self.subsection is not None else (self.section, name)
            )
            print(f"\"{dotted_path}\" doesnt exist in that yaml section/subsection idiot")
            raise AttributeError(repr(name)) from e

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __iter__(self):
        for name in self.__annotations__:
            yield name, getattr(self, name)

class Settings(metaclass=YAMLParser):
    section = "game_settings"

class Fmt:
    H_RED = "\033[101m"
    H_BLUE = "\033[104m"
    H_BLACK = "\033[40m"
    H_GRAY = "\033[100m"
    H_LGRAY = "\033[47m"
    H_LLGRAY = "\033[107m"

    T_RED = "\033[91m"
    T_BLUE = "\033[94m"
    T_BLACK = "\033[30m"
    T_GRAY = "\033[90m"
    T_LGRAY = "\033[37m"
    T_LLGRAY = "\033[97m"
    
    T_INVIS = "\033[8m"
    T_BLINKING = "\033[5m"