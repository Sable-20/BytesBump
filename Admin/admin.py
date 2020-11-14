import yaml

class Files:
  def config(a, b):
    with open("Admin/config.yml", "r") as f:
      return yaml.load(f, Loader=yaml.FullLoader)[a][b]
  
  def read(path):
    with open(path, "r") as f:
      return f.read()

  def get(file):
    with open(f"Admin/{file}.yml", "r") as f:
      return yaml.load(f, Loader=yaml.FullLoader)

  def emoji(emoji):
    return Files.config("emojis", emoji)