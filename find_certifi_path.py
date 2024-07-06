import certifi
import os

certifi_path = certifi.where()
# Set the location of the CA certificates file
os.environ['REQUESTS_CA_BUNDLE'] = certifi_path

print(f"The path to certifi CA certificates file is: {certifi_path}")
