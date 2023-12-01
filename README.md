# Python-Data-Acoustic-Modeling
This is a project for COP 2080, CS Problem Solving and Solution. We used the skills from this class to model the acoustics of an enclosed space.

# About the Project
It's evident that some indoor spaces have better acoustics than others, this project deals with voice and audio intelligibility within these spaces. With the use of
Python, we have created a tool to help improve audio intelligibility. For this project, we recorded sample audio from the Aula Magna, an indoor auditorium that has at
least 1 second of reverb time.

Our first step was to create a clean and simple GUI that was user-friendly and easily understood. We used Tkinter, a standard GUI toolkit for Python to create the GUI
that our user will fetch their desired audio sample from. We added a button that allows the user to access their files and select their audio file. The accepted file
types are .mp3 and .wav, however, to manipulate and plot this data (this will be discussed later) we will need to convert the audio file to the .wav file format.

After selecting the audio sample and converting it, we will manipulate and plot the audio in several different ways. We will remove the meta data, isolate the audio and plot it using SciPy. We will graph several different aspects of the audio file.

# Installation
**In order to use this project properly, you must pip-install these libraries:**
  - tkinter (to create the GUI)
  - pydub (used for converting and manipulating the audio)
  - ffmpeg (pydub works because of this framework, so it must be installed for pydub to work)
  - scipy (manipulation and plotting audio)

# Usage
**Follow these steps to use our project:**
  1. Ensure that you have all the necessary libraries installed
  2. Run the program (you should now see the GUI)
  3. Click on the "Select Audio File" button and select your audio sample
