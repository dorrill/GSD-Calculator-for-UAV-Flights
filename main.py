# GSD-Calculator for UAV Flights
# Author: 21satspleb
import os
import json

class Camera_Database:
  def __init__(self):
    """
    Initializes the Camera_Database class.
    """
    # Create camera database json if not exist in path
    if not os.path.exists(os.path.join(os.getcwd(), 'camera_database.json' )):
      # Create camera dict with example parameter based on Camera class
      self.camera_database = {'Zenmuse P1 35mm': {'sensor_width_px': 8192, 'sensor_height_px': 5460,
                                                  'pixel_size_nm': 4.27, 'focal_length_mm': 35}} 
      # Save camera database as .json on wkdir
      with open(os.path.join(os.getcwd(), 'camera_database.json'), 'w') as f:
        json.dump(self.camera_database, f)
      print(f'Camera database created at {os.getcwd()}')
    else:
      # Load camera database from.json on wkdir
      with open(os.path.join(os.getcwd(), 'camera_database.json'), 'r') as f:
        self.camera_database = json.load(f)
      print(f'Camera database loaded from {os.getcwd()}')
      # List camaras in camera database
      print(f'Cameras in database: {list(self.camera_database.keys())}')
  
  def add_camera(self, camera_name, sensor_width_px, sensor_height_px, pixel_size_nm, focal_length_mm):
    """
    Add camera to camera database
    """
    self.camera_database[camera_name] = {'sensor_width_px': sensor_width_px,'sensor_height_px':
                                         sensor_height_px, 'pixel_size_nm': pixel_size_nm,
                                         'focal_length_mm': focal_length_mm}
    # Save camera database as.json on wkdir
    with open(os.path.join(os.getcwd(), 'camera_database.json'), 'w') as f:
      json.dump(self.camera_database, f)
      print(f'Camera database updated at {os.getcwd()}')

  def get_list_cameras(self):
    """
    Get list of cameras in camera database
    """
    # List cameras in camera database
    return list(self.camera_database.keys())

  def get_camera_data(self, camera_name):
    """
    Get camera data from camera database
    """
    # Get camera data from camera database
    return self.camera_database[camera_name]
  

# class Camera:
#     def __init__(self,name, sensor_width_px, sensor_height_px, pixel_size_nm, focal_length_mm):
#       """
#       Initializes the camera class with the name, sensor width and height, pixel size and focal length.
#       """
#       self.name = name #Camera name
#       self.sensor_width_px = sensor_width_px #Sensor width in pixels
#       self.sensor_height_px = sensor_height_px #Sensor height in pixels
#       self.pixel_size_nm = pixel_size_nm #Sensor pixel size in nanometers
#       self.focal_length_mm = focal_length_mm #Sensor focal length in millimeters
#     def __repr__(self):
#       """Returns a string representation of the camera."""""
#       return "Camera: " + self.name + " \n Sensor Width: " + str(self.sensor_width_px) + " px \n Sensor Height: " + str(self.sensor_height_px) + " px \n Pixel Size: " + str(self.pixel_size_m) + " m \n Focal Length: " + str(self.focal_length_m) + " m"

class GSDCalculator:
  """
  Calculates the GSD (Ground Sampling Distance) for a set of camera parameters or the flight-height for a given GSD based on a set of camera parameters.
  """
  @staticmethod
  def calculate_gsd(altitude_m, sensor_width_px, pixel_size_nm, focal_length_mm):
    """
    Calculates the GSD for a given altitude and camera parameters.
    
    Parameters:
      altitude (float): Altitude in meters
      sensor_width_px (integer): Sensor width in pixels
      pixel_size_nm (float): Sensor pixel size in nanometers
      focal_length_mm (float): Sensor focal length in millimeters
    """
    pixel_size_m = pixel_size_nm / 1000000 # Convert nanometre to meter
    sensor_width_m = sensor_width_px * pixel_size_m # Calculate senor width in meters
    focal_length_m = focal_length_mm / 1000 # Convert millimeter to meter    
    gsd_m = (altitude_m * sensor_width_m) / (sensor_width_px * focal_length_m)
    gsd_cm = gsd_m * 100 # Convert meter to centimeter
    return gsd_cm
  @staticmethod
  def calculate_altitude(gsd_cm, sensor_width_px, pixel_size_nm, focal_length_mm):
    """
    Calculates the altitude for a given GSD and camera parameters.
    
    Parameters:
      gsd_cm (float): Ground Sampling Distance in centimeters
      sensor_width_px (integer): Sensor width in pixels
      pixel_size_nm (float): Sensor pixel size in nanometers
      focal_length_mm (float): Sensor focal length in millimeters
    """
    pixel_size_m = pixel_size_nm / 1000000 # Convert nanometre to meter
    sensor_width_m = sensor_width_px * pixel_size_m # Calculate senor width in meters
    focal_length_m = focal_length_mm / 1000 # Convert millimeter to meter
    gsd_m = gsd_cm / 100 # Convert centimeter to meter
    altitude_m = ( gsd_m * sensor_width_px * focal_length_m) / sensor_width_m 
    return altitude_m

def main():
  """
  Main function.
  """
  # Initialize camera database object
  camera_database = Camera_Database()

  def select_camera(camera_database):
    # List the available camera and prompt the user to select one
    camera_list = camera_database.get_list_cameras()
    # Print a numbered list of the cameras in camera_list  
    print("Camera List:")
    for i in range(len(camera_list)):
      print(str(i) + ": " + camera_list[i])      
    # Prompt the user to select a camera
    camera_index = input("Select a camera or B for back: ")    
    # Validate user input to make sure its a possitive integer
    if camera_index == "B":
      display_menu()
    else:
      camera_index = int(camera_index)      
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
  
  def trigger_gsd_calculator():
    """
    Triggers the GSD calculator.
    """
    # Call select_camera function to get the camera and camera parameters
    camera, camera_parameters = select_camera(camera_database)

    def prompt_altitude():
      # Promt for new altitude or to go back
      print("Enter B to go back or a altitude: ")
      altitude_m = input()
      if altitude_m == "B":
        trigger_gsd_calculator()
      else:
        altitude_m = float(altitude_m)
        return altitude_m
        
    def calculate_gsd(altitude_m, camera_parameters):
      # Calculate GSD for the given altitude and camera parameters
      gsd_cm = GSDCalculator.calculate_gsd(altitude_m, camera_parameters["sensor_width_px"],
                                           camera_parameters["pixel_size_nm"], camera_parameters["focal_length_mm"])
      # Print the GSD in centimeters
      print("GSD: " + str(round(gsd_cm, 2)) + "cm" + " at altitude of: " + str(round(altitude_m, 2)))

    altitude_m = prompt_altitude()
    calculate_gsd(altitude_m, camera_parameters)
    

    
    
    
    



  
  
  def display_welcome_message():
    program_title = "GSD Calculator for UAV Flights"
    author_name = "21satspleb"
    creation_date = "2023-05-12"
    program_description = ("This program allows users to calculate the Ground Sampling Distance "
                           "(GSD) for UAV flights. Users can select from a database of drone cameras, "
                           "add new cameras, and calculate either the GSD for a given flight altitude "
                           "or the required flight altitude for a desired GSD.")
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

  def display_menu():
    print("""Select an option from the menu below:
===============================================================
1. Calculate GSD for a given flight altitude
2. Calculate flight altitude for a given GSD
3. List available cameras
4. Add a new camera
===============================================================""")
    # Prompt user for input
    user_input = input("Enter your choice: ")
    # Validate user input
    if user_input == "1":
      trigger_gsd_calculator()
    elif user_input == "2":
      print("Calculating flight altitude for a given GSD...")
    elif user_input == "3":
      print("Listing available cameras...")
    elif user_input == "4":
      print("Adding a new camera...")
    else:
      print("Invalid choice.")
      display_menu()  
  
  display_welcome_message()
  display_menu()

    
if __name__ == "__main__":
    main()









# gsd_cm = GSDCalculator.calculate_gsd(100, 8192, 4.27, 35)
# alt = GSDCalculator.calculate_altitude(gsd_cm, 8192, 4.27, 35)
# print(gsd_cm, " - ", alt)

# test_database = Camera_Database()

# print(test_database.get_list_cameras())
