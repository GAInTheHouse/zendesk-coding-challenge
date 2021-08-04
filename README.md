# zendesk-coding-challenge

To run this project, python needs to be installed.

This project was developed on [GCC 8.4.0] linux with Python 3.6.9.

This project also utilizes several python libraries that need to be installed externally. These can be installed using pip. 

This project installed its dependancies through a pip version of 21.0.1.

These libraries have been listed in requirements.txt and can be installed using the command below:

```

pip3 install -r requirements.txt

```

To run the code, open the command line interface, and run:

```

python3 main.py USERNAME PASSWORD

```

To test this code, open the command line interface, and run:

```

py.test tester.py --username USERNAME --password PASSWORD

```

In both cases replace USERNAME and PASSWORD with the provided credentials

This project has also been deployed as a background process in the development environment (Google Cloud linux VM) and can be accessed using the link below:

```

http://146.148.93.178:5000/

```