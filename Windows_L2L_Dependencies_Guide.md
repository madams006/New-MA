# Windows L2L Dependencies Guide

Welcome to this guide/walkthrough on getting your Windows PC Ready to perform computation on the various tools and packages we have used thus far at L2L. With much of this work being on the bleeding edge of the bleeding edge, the packages can change rather quickly, and the initial set up can be quite a headache. With this guide, I hope to make the setup of your pc much more accessible, and allow for actual work to be completed, rather than hours spent reinstalling.

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

First, find out what Python version you have within your environment, you can run  'python --version'

Next, go to this page: http://www.open3d.org/docs/release/getting_started.html 

We are looking for the development version (pip) section: 