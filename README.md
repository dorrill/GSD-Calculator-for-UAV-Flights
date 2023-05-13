# GSD Calculator for UAV Flights
This is a Python script that calculates the Ground Sampling Distance (GSD) for an Unmanned Aerial Vehicle (UAV). The GSD is the distance between two consecutive pixels on the ground, and it is an important parameter for capturing high-quality aerial images. This script allows you to calculate the GSD based on a set of camera parameters or the flight altitude for a given GSD.

## Features
The GSD Calculator has the following features:

1. Calculate GSD for a given flight altitude
2. Calculate flight altitude for a given GSD
3. List available cameras in the database
4. Add a new camera to the database
   
## Installation
To run this script, you need Python 3.x installed on your computer. You can download the latest version of Python from the official website: https://www.python.org/downloads/

You will also need to install the following packages:

* os
* json
  
These packages are included with Python, so you do not need to install them separately.

## Usage
To use the GSD Calculator, simply run the main.py file in your favorite Python environment or from the terminal with the command python main.py.

The script will display a menu with the available options. You can select an option by entering the corresponding number.

1. To calculate the GSD for a given altitude and camera parameters, select option 1 and follow the prompts.

2. To calculate the flight altitude for a given GSD and camera parameters, select option 2 and follow the prompts.

3. To view a list of all cameras in the camera database, select option 3.

4. To add a new camera to the camera database, select option 4 and follow the prompts.

## Getting Started

To use the GSD Calculator, you'll need a Python environment. Once you have that set up, download the program and run it. You'll be prompted with a menu of options, and you can choose to calculate GSD, flight altitude, list available cameras, or add a new camera.

## Required Camera Parameters
The following parameters of the camera used on the UAV are required for the GSD Calculator:

* **Sensor Width** (in pixel): The width of the camera sensor. This information can be usually found in the camera specifications.
* **Sensor Height** (in pixel): The height of the camera sensor. This information can be usually found in the camera specifications.
* **Pixel Size** (in nm): The size of an individual pixel in nanometer.
* **Focal Length** (in millimeters): The distance between the camera sensor and the lens. This information is typically provided in the camera specifications.

## GSD Calculation

The Ground Sampling Distance (GSD) is the distance between two consecutive pixel centers measured on the ground. The formula used to calculate GSD is:

GSD = (Sensor Width * Altitude) / (Focal Length * Image Width)


Where:

- **GSD** is the Ground Sampling Distance, expressed in meter/pixel.
- **Sensor Width** is the width of the camera sensor, in meter.
- **Altitude** is the flying altitude of the drone, in meters.
- **Focal Length** is the distance between the camera sensor and the lens, in meter.
- **Image Width** is the horizontal size of the image, in pixels.

The smaller the GSD, the higher the image resolution, hence more details can be identified.

## Flight Altitude Calculation

The required flight altitude to achieve a specific GSD is calculated using the rearranged GSD formula:

Altitude = (GSD * Focal Length * Image Width) / Sensor Width


Where:

- **Altitude** is the flying altitude of the drone, in meters.
- **GSD** is the Ground Sampling Distance, expressed in meters/pixel.
- **Focal Length** is the distance between the camera sensor and the lens, in meters.
- **Image Width** is the horizontal size of the image, in pixels.
- **Sensor Width** is the width of the camera sensor, in meters.


## Contributing

Contributions are welcome! If you would like to contribute to this project, please fork this repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.