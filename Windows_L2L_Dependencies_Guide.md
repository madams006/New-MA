# Windows L2L Dependencies Guide

Welcome to this guide/walkthrough on getting your Windows PC Ready to perform computation on the various tools and packages we have used thus far at L2L. With much of this work being on the bleeding edge of the bleeding edge, the packages can change rather quickly, and the initial set up can be quite a headache. With this guide, I hope to make the setup of your pc much more accessible, and allow for actual work to be completed, rather than hours spent reinstalling.

## The L2L_Toolset Files & A Quick Note

Within the L2L_Toolset, you will find the l2ltools.py, as well as an initialize_config.py. From there, these files will provide you with much of the same functionality as is used in the Body-Segmentation Notebooks, and are similar to some of the more recent versions and implementations. The more recent demo of this segmentation is built on object-oriented programming, however the core usage of the functions should remain the same/similar. You will also find a testing_l2ltools_library python notebook, which just shows how simple the implementation of these tools becomes as you further along the project in working on pointclouds. This simply allows for cleaner coding, as we can call ```from l2ltools.py import *``` to import all of our necessary functions, and begin working from there.

With that said, I'd like to jump right into the steps for getting you working on the project; also, if anyone has any issues, please feel free to ping me on Slack, or reachout at madams006@regis.edu; I should still be checking it regularly, and I am happy to help, as I spent multiple weeks plagued by errors when starting this project. 

## Beginning Steps

To begin, I will have attached my actual Conda Environment file here ##INSERT LINK to YML env file here##, which will have many of the dependencies already installed. While this will save what was in my case hours of installing the right dependencies, we still have some work left for us, as many of these packages require special versioning and other system dependencies we may not start with. 

Once you have downloaded my environment.yml ("l2l_env.yml"), please run the following command to create a conda environment from this. NOTE - please always use environments to manage dependencies, a harsh lesson this project has taught me is dependencies have different versions depedning on the project/work you are doing, so always the best practice is creating these virtual environments.

#### Run this command

conda env create --name YOUR_DESIRED_NAME_HERE --file l2l_env.yml

#### Once you have ran this successfully, open a command prompt and run:

conda activate YOUR_DESIRED_NAME_HERE 

#### You can confirm this is working by running a simple Jupyter notebook in Jupyter or VSC (or similar) and just importing common packages, such as Pandas or Numpy

Next, we will get to the more difficult to work with dependencies that I simply couldn't include with the environment, as they are changing and dependent on your environment. I also found over weeks of struggle that we must use Open3d's developmental version, or our k4a will not run no matter how much willpower or man-hours is thrown at it (trust me).

#### Installing Open3D

This is a big one, as I said above, as without it nothing will run. Much of our work thus far has been in part due to this library. As mentioned above, so we need to get the developmental version, meaning we cannot just pip install open3d.

First, find out what Python version you have within your environment, you can run  `python --version`

Next, go to this page: http://www.open3d.org/docs/release/getting_started.html 

We are looking for the development version (pip) section: ![open3d Development Image](/images/open3d_install_dev.PNG)

Depending on what your `python --version` returned, please select that version from the table. We will right click on the version, and copy the link url. Mine looked like this: https://storage.googleapis.com/open3d-releases-master/python-wheels/open3d-0.15.1-cp38-cp38-win_amd64.whl 

To install this into our environment, we will go back to our command prompt, or open a new one if we closed it. If we closed our commad prompt, make sure to conda activate YOUR_DESIRED_NAME_HERE before completing this step. Once we have ensured we are in our L2L environment, run this:

`pip install $$YOUR COPIED URL`

so, for me:

`pip install https://storage.googleapis.com/open3d-releases-master/python-wheels/open3d-0.15.1-cp38-cp38-win_amd64.whl`

this will pip install direct from this location. We now have successfully installed the correct developmental version of Open3d, which as of April 2022 works with our notebooks.

#### Installing our K4A Drivers and PyK4a Packages

Next, we will be installing the actual K4A Drivers, as well as the PyK4a Python wrapper for k4a. K4A comes from the Azure Kinect SDK Microsoft Kit, which has some good documentation to follow and utilize as you work on the project. 

Go to https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md and install v1.4.1 by clicking on the MSI Azure Kinect SDK 1.4.1.exe

This will put all your k4a drivers, by default into C:\Program Files\Azure Kinect SDK version\sdk

We now want to ensure we add these k4a drivers to our Path Variable - Yours should look something similar to this:

![Environment Path Variable](/images/Path_Variables.PNG)

##### PyK4a Python Wrapper for K4A

This is definitely the most troublesome step going through this a second time, as the error messages can be misleading as to the root issue. Below, I will put a few of the errors you may see; **If you see any of these errors, please see below's steps, which should fix them**

![pyk4a before drivers error](/images/pyk4a_before.PNG)

If you see this image, please ensure you have installed the K4A Drivers Above, as well as added K4A to your Environment Path.

![Microsoft C Error](/images/Microsoft_C_Error.PNG)

If you see this error, it means your Microsoft C++ Tool isn't up to date. 
**NOTE That if your Microsoft C++ Tool is up to or past 14.0, you need to ensure you have the proper modules with-in the kit. Run the installer again, and select the Desktop Development Kit:**

![Select This Microsft C++](/images/select_this_c.PNG)


## Common Error Messages

Firstly, if you haven't read everything above this line, please do so first, as you will find several answers there to many of the issues you may encounter. With that said, below are some of the more unique error messages that you may experience working on this project. 

#### Memory Error when Working on AWS EC2 Instance

This below error is something both I and Matt received on different operations within the AWS EC2 instance - the fix is below:

https://www.codegrepper.com/code-examples/whatever/413+request+entity+too+large

The command is ```sudo nano /etc/nginx/nginx.conf``` to edit and add this line - ```client_max_body_size 400M``` - this will require Sudo access, which if you do not have just reach out to Jim Reed. For more information, see the link above, but that alone should fix it.

![AWS EC2 Memory_Error](/images/memory_error.PNG)