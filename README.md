# ME500_VISION
Welcome to our READ ME for our FFF Machine Vision Error Detection Project!

This is the place where you can find all of the information on our files that we've developed over the past couple of months to get up to speed.

## File Organization and Helpful Links

Four folders show our journey through this project: References, Roboflow_Integration, Raspberry Pi Integration, and Email_Integration. The References folder gives the scripts from an OpenCV Bootcamp that is linked [here](https://courses.opencv.org/courses/course-v1:OpenCV+Bootcamp+CV0/course/). Going through this was pretty helpful when it came to relearning Python and getting up to speed with OpenCV's image-processing capabilities even though it is used pretty sparsely in our scripts. The Roboflow Integration folder contains the scripts that we used to familiarize ourselves with the Roboflow API and how we integrated it into our application. Here are some links that we've found helpful and are a good introduction to the platform: 
[Deploy your Roboflow Train models to Raspberry Pi.](https://docs.roboflow.com/deploy/legacy-documentation/raspberry-pi) 
[Roboflow Documentation](https://docs.roboflow.com/)

Next, we used a Raspberry Pi 4 to run our application. To use your time efficiently, ensure that you are familiar with how code is executed on a Raspberry Pi (i.e. using virtual environments, how to install necessary libraries, etc.)

[Create a Python virtual environment](https://raspberrypi-guide.github.io/programming/create-python-virtual-environment). 

Using a virtual environment within a folder in your directory makes sure that all of the libraries you install for a project stay organized. This is good practice across the board if you're new to writing software.

To transfer files between our computers and the Raspberry Pi remotely, we used FileZilla over an SSH connection. You can download that  [here](https://filezilla-project.org/download.php). We also used Putty to run scripts remotely on the Raspberry Pi over an SSH connection. Download that [here](https://www.putty.org/).

Also, here are some YouTube videos that helped us immensely in understanding how to work with computer vision models on the RasPi:
[Beginner Tutorial: How to Stream Video from Raspberry Pi Camera to Computer using Python (P2)](https://www.youtube.com/watch?v=p4L3g9Grl3k)
[How to Deploy Computer Vision Models to Raspberry Pi with Docker](https://www.youtube.com/watch?v=S-Ga_uxnRZA)

Lastly, we have Email Integration. Ideally, the user would receive an email with an attachment including the annotated image of their failed print. However, what we have currently sends an email with the necessary objects (To, From, Body). 

Overall, we hope this application can detect, pause or stop a failed print, and notify the user of the failure by whatever means necessary. If any questions arise, my email is mpbcowley@gmail.com.
