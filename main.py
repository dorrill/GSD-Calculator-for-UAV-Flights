# GSD-Calculator for UAV Flights
# Author: Orinal author: 21satspleb, Revised by Ryan Dorrill - dorrill1@gmail.com

import os
import json

# Constants

uM_TO_M = 1e-6  # nanometers to meters --> #Ryan's note - Bro mixed up um and nm....whoops
MM_TO_M = 1e-3  # millimeters to meters
CM_TO_M = 100  # millimeters to meters

class Camera_Database:
  def __init__(self):
    """
    Initializes the Camera_Database class and loads the camera database from a JSON file
    if it exists. If not, creates a new one with example data.
    """
    self.camera_database_path = os.path.join(os.getcwd(), 'camera_database.json')
    # Create camera database json if not exist in path
    if not os.path.exists(self.camera_database_path):
      # Create camera dict with example parameter based on Camera class
      self.camera_database = {'Zenmuse P1 35mm': {'sensor_width_px': 8192, 'sensor_height_px': 5460,
                                                  'pixel_size_um': 4.27, 'focal_length_mm': 35}}
      # Save camera database as .json on wkdir
      with open(self.camera_database_path, 'w') as f:
        json.dump(self.camera_database, f)
    else:
      # Load camera database from.json on wkdir
      with open(self.camera_database_path, 'r') as f:
        self.camera_database = json.load(f)


  def add_camera(self, camera_name, sensor_width_px, sensor_height_px, pixel_size_um, focal_length_mm):
    """
    Adds a new camera to the camera database and updates the JSON file.

    Args:
      camera_name (str): The name of the camera.
      sensor_width_px (int): The width of the sensor in pixels.
      sensor_height_px (int): The height of the sensor in pixels.
      pixel_size_um (float): The size of each pixel in nanometers.
      focal_length_mm (float): The focal length of the camera in millimeters.
    """
    self.camera_database[camera_name] = {'sensor_width_px': sensor_width_px,'sensor_height_px':
                                         sensor_height_px, 'pixel_size_um': pixel_size_um,
                                         'focal_length_mm': focal_length_mm}
    # Save camera database as.json on wkdir
    with open(self.camera_database_path, 'w') as f:
      json.dump(self.camera_database, f)
      print(f'Camera database updated at {os.getcwd()}')

  def get_list_cameras(self):
    """
    Gets a list of all cameras in the camera database.

    Returns:
      list: A list of all camera names in the camera database.
    """
    # List cameras in camera database
    return list(self.camera_database.keys())

  def get_camera_data(self, camera_name):
    """
    Gets the data for a specific camera from the camera database.

    Args:
      camera_name (str): The name of the camera to get data for.

    Returns:
      dict: A dictionary containing the data for the camera.

    Raises:
      KeyError: If the camera_name is not found in the camera database.
    """
    try:
      return self.camera_database[camera_name]
    except KeyError:
      print(f"Camera {camera_name} not found in the database.")
      return None

class GSDCalculator:
  """
  Calculates the GSD (Ground Sampling Distance) for a set of camera parameters or the flight-height for a given GSD based on a set of camera parameters.
  """

  @staticmethod
  def calculate_gsd(altitude_m, sensor_width_px, pixel_size_um, focal_length_mm):
    """
        Calculates the Ground Sampling Distance (GSD) for a given altitude and camera parameters.

        Args:
            altitude_m (float): The flight altitude in meters.
            sensor_width_px (int): The sensor width in pixels.
            pixel_size_um (float): The sensor pixel size in nanometers.
            focal_length_mm (float): The sensor focal length in millimeters.

        Returns:
            float: The calculated GSD in centimeters.
        """
    pixel_size_m = pixel_size_um * uM_TO_M   # Convert nanometre to meter
    sensor_width_m = sensor_width_px * pixel_size_m # Calculate senor width in meters
    focal_length_m = focal_length_mm * MM_TO_M # Convert millimeter to meter
    gsd_m = (altitude_m * sensor_width_m) / (sensor_width_px * focal_length_m)
    gsd_cm = gsd_m * CM_TO_M # Convert meter to centimeter
    return gsd_cm

  @staticmethod
  def calculate_altitude(gsd_cm, sensor_width_px, pixel_size_um, focal_length_mm):
    """
        Calculates the flight altitude for a given Ground Sampling Distance (GSD) and camera
        parameters.

        Args:
            gsd_cm (float): The Ground Sampling Distance in centimeters.
            sensor_width_px (int): The sensor width in pixels.
            pixel_size_um (float): The sensor pixel size in nanometers.
            focal_length_mm (float): The sensor focal length in millimeters.

        Returns:
            float: The calculated flight altitude in meters.
        """
    pixel_size_m = pixel_size_um * uM_TO_M # Convert nanometre to meter
    sensor_width_m = sensor_width_px * pixel_size_m # Calculate senor width in meters
    focal_length_m = focal_length_mm * MM_TO_M # Convert millimeter to meter
    gsd_m = gsd_cm / CM_TO_M # Convert centimeter to meter
    altitude_m = ( gsd_m * sensor_width_px * focal_length_m) / sensor_width_m
    return altitude_m

def clear_console():
    """
    Clear console
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_input(user_input, min_value=None, max_value=None, expected_types=None):
    """
    Validates the user input.

    Args:
        user_input (any): The user's input.
        min_value (Optional[int or float]): The minimum value that the input should have (inclusive).
        max_value (Optional[int or float]): The maximum value that the input should have (inclusive).
        expected_types (Optional[Iterable[type]]): The expected types of the input str, int ot float.

    Returns:
        bool: True if the input is valid, False otherwise.

    Raises:
        ValueError: If the input value cannot be converted to the expected types.

    """
    if expected_types is None:
        expected_types = [str, int, float]  # Sequence changed here

    for expected_type in expected_types:
        try:
            if expected_type == str:
                value = str(user_input)
            elif expected_type == int:
                # Check if the input is a whole number
                if user_input.isdigit():
                    value = int(user_input)
                else:
                    raise ValueError
            elif expected_type == float:
                # Check if the input is a float number
                value = float(user_input)
            else:
                raise ValueError

            if min_value is not None and value < min_value:
                print(f"Invalid input. The value should be greater than or equal to {min_value}.")
                return False

            if max_value is not None and value > max_value:
                print(f"Invalid input. The value should be less than or equal to {max_value}.")
                return False

        except ValueError:
            continue
        else:
            return True

    print("Invalid input. Please enter a valid input.")
    return False

def add_cam(camera_database):
  """
  Adds a camera to the camera database based on user input.

  Args:
      camera_database (Camera_Database): The Camera_Database object to add the camera to.

  Returns:
      None

  """
  camera_name = input("Enter camera name [B for back]: ")
  if camera_name.lower() == "b":
    display_welcome_message()
    display_menu(camera_database)
    return


  # Prompt the user to enter sensor width in pixels
  is_valid = False
  while is_valid == False:
    sensor_width_px = input("Enter sensor width in pixels [B for back]: ")
    if sensor_width_px.lower() == "b":
      display_welcome_message()
      display_menu(camera_database)
      return # return from the function if the user wants to go back
    is_valid = validate_input(sensor_width_px, min_value=1, max_value=100000, expected_types=[int])
    if is_valid:
      sensor_width_px = int(sensor_width_px)

  # Prompt the user to enter sensor_height in pixels
  is_valid = False
  while is_valid == False:
    sensor_height_px = input("Enter sensor height in pixels [B for back]: ")
    if sensor_height_px.lower() == "b":
      display_welcome_message()
      display_menu(camera_database)
      return # return from the function if the user wants to go back
    is_valid = validate_input(sensor_height_px, min_value=1, max_value=100000, expected_types=[int])
    if is_valid:
      sensor_height_px = int(sensor_height_px)

  # Prompt the user to enter pixel size in nanometers
  is_valid = False
  while is_valid == False:
    pixel_size_um = input("Enter pixel size in nanometers [B for back]: ")
    if pixel_size_um.lower() == "b":
      display_welcome_message()
      display_menu(camera_database)
      return
    is_valid = validate_input(pixel_size_um, min_value=1, max_value=100000, expected_types=[int,float])
    if is_valid:
      pixel_size_um = float(pixel_size_um)

  # Prompt the user to enter focal length in millimeters
  is_valid = False
  while is_valid == False:
    focal_length_mm = input("Enter focal length in millimeters [B for back]: ")
    if focal_length_mm .lower() == "b":
      display_welcome_message()
      display_menu(camera_database)
      return
    is_valid = validate_input(focal_length_mm, min_value=1, max_value=1500, expected_types=[int,float])
    if is_valid:
      focal_length_mm = float(focal_length_mm)

  # Add camera to database
  camera_database.add_camera(camera_name, sensor_width_px, sensor_height_px, pixel_size_um, focal_length_mm)
  # Print success message
  print("Camera added successfully.")
  display_menu(camera_database)

def select_camera(camera_database):
  """
  Allows the user to select a camera from the camera database.

  Args:
      camera_database (Camera_Database): The Camera_Database object containing the camera database.

  Returns:
      tuple: A tuple containing the selected camera name and its parameters.

  """
  # List the available camera and prompt the user to select one
  camera_list = camera_database.get_list_cameras()
  # Print a numbered list of the cameras in camera_list
  print("Camera List:")
  for i in range(len(camera_list)):
    print(str(i) + ": " + camera_list[i])
  # Prompt the user to select a camera
  camera_index = input("Select a camera or B for back: ")
  # Validate user input to make sure its a possitive integer
  if camera_index.lower() == "b":
    display_menu(camera_database)
  if camera_index.isdigit():
    camera_index = int(camera_index)
  else:
    print("Invalid input. Please enter a valid number.")
    select_camera(camera_database)
  if camera_index < 0 or camera_index >= len(camera_list):
    print("Invalid camera selection.")
    select_camera(camera_database)
  # Get the camera object from the camera list
  camera = camera_list[camera_index]
  # Get camera parametzers from database
  camera_parameters = camera_database.get_camera_data(camera)
  # Print selected camera name and its parameters
  print("Selected camera: " + camera + " - " + str(camera_parameters))
  return camera, camera_parameters

def list_cameras(camera_database):
  """
  Displays the available cameras from the camera database and prompts the user to select one.

  Args:
      camera_database (Camera_Database): The Camera_Database object containing the camera database.

  Returns:
      None

  """
  # List the available camera and prompt the user to select one
  camera_list = camera_database.get_list_cameras()
  # Print a numbered list of the cameras in camera_list
  print("Camera List:")
  for i in range(len(camera_list)):
    print(str(i) + ": " + camera_list[i])
  # Prompt the user to select a camera
  input("Any key for back: ")
  # Validate user input to make sure its a possitive integer
  display_menu(camera_database)

def trigger_gsd_calculator(camera_database):
  """
    Triggers the GSD calculator. Prompts the user to select a camera from the database and
    to enter the flight altitude. The function then calculates and displays the GSD.

    Note: This function doesn't take any arguments, so we don't have an 'Args:' section in the docstring.

    Returns:
        None

    """
  # Call select_camera function to get the camera and camera parameters
  camera, camera_parameters = select_camera(camera_database)

  # Continously prompt for new altitudes until the user writes B
  stillWorking = 'y'
  while stillWorking.lower() == 'y':
      """
    Prompts the user for a new altitude or to go back.

    Returns:
        float: The entered altitude in meters.
    """
    # Promt for new altitude or to go back
      print("Enter the altitude in meters, or B to go back: ")
      altitude_m = input()
      if altitude_m.lower() == "b":
        stillWorking = 'n'
      if altitude_m.isdigit():
        altitude_m = float(altitude_m)
        # Validate user input to make sure its a positive float
        if not validate_input(altitude_m, min_value=0, max_value=2000000,
                              expected_types=[float]):
            return prompt_altitude()
        calculate_gsd(altitude_m, camera_parameters)
      else:
        print("Invalid input.")


def calculate_gsd(altitude_m, camera_parameters):
      """
      Calculates the Ground Sampling Distance (GSD) for the given altitude and camera parameters.

      Args:
          altitude_m (float): The altitude in meters.
          camera_parameters (dict): The parameters of the selected camera.

      Returns:
          None

      """
      # Calculate GSD for the given altitude and camera parameters
      gsd_cm = GSDCalculator.calculate_gsd(altitude_m, camera_parameters["sensor_width_px"],
                                           camera_parameters["pixel_size_um"],
                                           camera_parameters["focal_length_mm"])
      # Print the GSD in centimeters
      print("GSD: " + str(round(gsd_cm, 2)) + "cm" + " at altitude of: " + str(round(altitude_m,2)))

def trigger_altitude_calculator(camera_database):
  """
  Triggers the Altitude calculator.

  Args:
      camera_database (Camera_Database): The Camera_Database object containing the camera database.

  Returns:
      None

  """
  # Call select_camera function to get the camera and camera parameters
  camera, camera_parameters = select_camera(camera_database)
  stillWorking = 'y'
  while stillWorking.lower() == 'y':
          """
      Prompts the user for a new GSD or to go back.

      Returns:
          float: The entered GSD in centimeters.

      """
          # Promt for new altitude or to go back
          print("Enter a GSD [cm] or B to go back: ")
          gsd_cm = input()
          if gsd_cm.lower() == "b" or gsd_cm.lower() == "q":
              stillWorking = 'n'
          elif gsd_cm.isdigit():
              gsd_cm = float(gsd_cm)
              # Validate user input to make sure its a positive float
              while not validate_input(gsd_cm, min_value=0, max_value=10000, expected_types=[float]):
                print("Invalid GSD... value should be in meters")
                print("Enter a GSD [cm] or B to go back: ")
                gsd_cm = input()

              calculate_alttitude(gsd_cm, camera_parameters)
          else:
              print("Invalid input.")
              return prompt_gsd()

def calculate_alttitude(gsd_cm, camera_parameters):
        """
      Calculates the altitude for the given GSD and camera parameters.

      Args:
          gsd_cm (float): The GSD in centimeters.
          camera_parameters (dict): The parameters of the selected camera.

      Returns:
          None

        """
        # Calculate altitude for the given gsd and camera parameters
        altitude_m = GSDCalculator.calculate_altitude(gsd_cm, camera_parameters["sensor_width_px"],
                                             camera_parameters["pixel_size_um"], camera_parameters["focal_length_mm"])
        # Print the altitudes in meters
        print("Altitude: " + str(round(altitude_m, 2)) + "m" + " at GSD of: " + str(round(gsd_cm, 2)) + " cm")

def display_welcome_message():
  """
  Displays the welcome message for the GSD Calculator program.

  Returns:
      None

  """
  program_title = "GSD Calculator for UAV Flights"
  author_name = "21satspleb"
  creation_date = "2023-05-12"
  program_description = ("This program allows users to calculate the Ground Sampling Distance "
                         "(GSD) for UAV flights. Users can select from a database of drone cameras, "
                         "add new cameras, and calculate either the GSD for a given flight altitude "
                         "or the required flight altitude (in meters) for a desired GSD.")
  drone_ascii = """                ⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿
              ⣿⣿⣿⡿⠿⠿⠿⠷⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠾⠿⠿⠿⢿⣿
              ⣿⣿⣿⣿⣿⣿⣿⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣿⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⣿⣿⣿⣿⣿⣡⣤⣤⣌⣿⣿⣿⣿⣿⠀⠀⠀⠀⠈⣿⣿⣿
              ⣿⣿⣿⣿⣿⣤⣤⣄⣀⣀⠀⠀⠀⢠⡾⢋⣤⣤⡙⢷⡄⠀⠀⠀⣀⣀⣠⣤⣤⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢷⣾⣧⡘⠿⠿⢃⣼⣷⡾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⢀⣴⣿⡉⠻⠶⠶⠟⢉⣿⣦⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⡿⠟⠁⣠⣴⣿⣿⣿⣷⣶⣶⣶⣶⣾⣿⣿⣿⣦⣄⠈⠻⢿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⠀⠀⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠀⠀⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣷⣄⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⣠⣾⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⢀⣴⣿⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡾⠿⢿⣿⣿⣿⣿⣿⣿⡿⠿⢷⣤⣾⣿⣿⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿
              ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿"""
  print(f"""
===============================================================
{drone_ascii}
===============================================================
Program Title: {program_title}
Author Name: {author_name}
Creation Date: {creation_date}
---------------------------------------------------------------
Program Description: {program_description}
===============================================================""")

def display_menu(camera_database):
  """
  Displays the menu for the GSD Calculator program and handles user input.

  Returns:
      None

  """

  continueRunning = 'y'
  while(continueRunning =='y'):
      print("""Select an option from the menu below:
    ===============================================================
    1. Calculate GSD for a given flight altitude
    2. Calculate flight altitude for a given GSD
    3. List available cameras
    4. Add a new camera
    5. Quit (q)
    ===============================================================""")
      # Prompt user for input
      user_input = input("Enter your choice: ")
      # Validate user input
      if user_input == "1":
        clear_console()
        trigger_gsd_calculator(camera_database)
      elif user_input == "2":
        clear_console()
        trigger_altitude_calculator(camera_database)
      elif user_input == "3":
        clear_console()
        list_cameras(camera_database)
      elif user_input == "4":
        clear_console()
        add_cam(camera_database)
      elif user_input == "5" or user_input.lower() == "q":
        clear_console()
        continueRunning = 'n'
        return 0
      else:
        clear_console()
        print("\""+ user_input + "\"" + " is an invalid choice. \n")
        display_welcome_message()
        display_menu(camera_database)

def main():
  """
  Main function.
  """
  # Initialize camera database object
  camera_database = Camera_Database()

  display_welcome_message()
  display_menu(camera_database)

if __name__ == "__main__":
    main()
