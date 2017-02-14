#-------------------------------------------------------------------------#
#                                    Makefile                             #
#                       Oscar Barragán, Jan. 2017                         #
#-------------------------------------------------------------------------#
#    make       -> compiles the code                                      #
#-------------------------------------------------------------------------#

FP=f2py
fc=gnu95 
cc=unix 

FLAGS= -c -m 
SOURCES= quad.f90 \
         findz.f90

EXECUTABLE=exomodule

all: $(EXECUTABLE) 
$(EXECUTABLE):$(SOURCES)
	${FP} ${FLAGS} $(EXECUTABLE) $(SOURCES)  --fcompiler=$(fc) --compiler=$(cc)

clean:
	rm $(EXECUTABLE).so
