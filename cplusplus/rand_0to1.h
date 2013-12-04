#ifndef _RAND_0TO1_H
#define _RAND_0TO1_H

#ifdef __cplusplus

extern "C"{
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>
#include <string.h>

double rand_0to1(int num)
{
       char *str;
       int i;
       double re = 0;
       assert(num > 0);
      // srand(time(0));
       str = (char *)malloc(3+num);
       strncpy(str,"0.",2);
       for( i = 0; i < num; i++){
            sprintf( str + 2 + i, "%d",rand() % 10 );
       }
       str[num + 2] = 0;
       re = atof(str) ;
       free(str);
       return re;
}
}

#endif

#endif
