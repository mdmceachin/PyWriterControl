# PyWriterControl
This application allows to control of histology cassettes and slide labelling machines (Thermo SlideWriter and Carousel MicroWriter). 

Thermo won't support them anymore and the current application (Shandon Microwriter) is not working properly. I had to develop this during my placement at NAMSA, for the sole purpose of simplifying the work of technicians here.

This mainly use Tkinter and ttk for the interface, and Pyserial for the serial interface communication. It also use collection, os, thread/multiprocessing, re, datetime, weakref and cx_freeze.
