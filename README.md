# Tag Counter
Written By Calum Lindsay.  
 It is a simple application to count the number of tags that have been printed by the Laser Printer we use at work. It is still very early in development acting as something of a Sandbox for me playing with Python and wxPython. There will be errors and it's very messy but it does mostly do what it's supposed to.

## How to run it
You will need Python and wxPython. Once you have them and assuming you are on windows open a command prompt, navigate to where tag-counter is and type py tag-counter.py. I would imagine linux is basically the same but my Debian system is out of comission at the moment and I've never used python on linux so I can't say for sure.

## Possible future improvements / problems

Unfinished Legacy Version

- [ ] Saving and loading of current state
- [ ] Tidy up & comments
- [x] Align status bar correctly
- [ ] Bug testing
- [ ] Tag code generation (ex. 08061202 == YPS(08), Vatsetter(05), 12(12th), 02(Feb))
- [ ] Store site and Packing station nubers in an editable file
- [ ] Move functions which only need to update on input out of update and into event handlers