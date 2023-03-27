import os
import urllib.request
import zipfile

# Step 1: Ask user to specify a file location
file_location = input("Please specify a file location: ")

# Step 2: Ask user for the name of modpack and create a folder
modpack_name = input("Please enter the name of your modpack: ")
modpack_folder = os.path.join(file_location, modpack_name)
if not os.path.exists(modpack_folder):
    os.makedirs(modpack_folder)

# Step 3: Ask user for modpack link, or skip if "o" is entered
modpack_link = input("Please enter the modpack download link: ")
if modpack_link.lower() != "o":
    modpack_zip_file = os.path.join(modpack_folder, os.path.basename(modpack_link))
    urllib.request.urlretrieve(modpack_link, modpack_zip_file)
    with zipfile.ZipFile(modpack_zip_file, 'r') as zip_ref:
        zip_ref.extractall(modpack_folder)
    os.remove(modpack_zip_file)

# Step 4: Ask user for Minecraft version and determine which Java image to use
minecraft_version = input("Please enter the version of Minecraft you are using (e.g. 1.16.5): ")
if float(minecraft_version[:4]) <= 1.16:
    minecraft_image = "itzg/minecraft-server:java8-multiarch"
else:
    minecraft_image = "itzg/minecraft-server"

# Step 5: Ask user for environment variables and create docker-compose file
environment_variables = {
    "TYPE": input("Enter the server type (vanilla/spigot/paper/etc.): "),
    "MAX_MEMORY": input("Enter the maximum memory allocation (e.g. 1G): "),
    "VERSION": minecraft_version,
    "PORT": input("Enter the port number to use (e.g. 25565): ")
}
with open(os.path.join(modpack_folder, "docker-compose.yml"), 'w') as file:
    file.write(f'''version: '3'
services:
  minecraft:
    image: {minecraft_image}
    environment:
      INIT_MEMORY: 512M
      DIFFICULTY: 1
      MAX_TICK_TIME: -1
      SPAWN_PROTECTION: 0
      USE_AIKARS_FLAGS: "true"
      RCON_PASSWORD: "minecraft"
      VIEW_DISTANCE: 10
      EULA: "true"
      ENFORCE_WHITELIST: "true"
      TYPE: {environment_variables["TYPE"]}
      MAX_MEMORY: {environment_variables["MAX_MEMORY"]}
      VERSION: {environment_variables["VERSION"]}
      PORT: {environment_variables["PORT"]}
    volumes:
      - {modpack_folder}:/data
    stdin_open: true
    tty: true
    restart: unless-stopped
''')

# Step 6: Ask user if they want to start the server using docker-compose
start_server = input("Do you want to start the server now? (yes/no): ")
if start_server.lower() == "yes":
    os.chdir(modpack_folder)
    os.system("docker-compose up -d")
