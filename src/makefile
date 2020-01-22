#-------------------------------------------------------------------------#
#                                    Makefile                             #
#                       Oscar Barragán, Jan. 2017                         #
#                       Updated, Oct. 2019                                #
#-------------------------------------------------------------------------#
#    make       -> compiles the code                                      #
#-------------------------------------------------------------------------#

#Check that you are compiling with the python version that you plan to use
FP=f2py2.7
#FP=f2py3.6

fc=gnu95 
cc=unix 

FLAGS= -c -m 
SOURCES= constants.f90 \
	 quad.f90 \
         findz.f90

EXECUTABLE=exomodule

all: $(EXECUTABLE) 
$(EXECUTABLE):$(SOURCES)
	${FP} ${FLAGS} $(EXECUTABLE) $(SOURCES)  --fcompiler=$(fc) --compiler=$(cc)

clean:
	rm $(EXECUTABLE).so
