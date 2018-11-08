#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>

int main (void)
{
  pid_t f;
  //int horse = 5;
  int *ptr = (int*) malloc(sizeof(int) * 1);
  *ptr = 3;
  f=fork();
  if (f==-1)
  {
    printf("Error \n");
    exit(1);
  } 
  else if (f==0)
  {
    printf("   Child: My process ID: %d \n", getpid());
    
    //printf("   Child horse: %d \n", horse);
    printf("   The Child ptr: %p and its value: %d \n", ptr, *ptr);
    *ptr = 2;
    sleep(1);
    //horse = 2;
    //printf("   I am child and new horse is: %d \n", horse);
    printf("   I am the child, ptr: %p and its value: %d \n", ptr, *ptr);

    printf("   Child: My parent's process ID: %d \n", getppid());
    exit(0);
  }
  else
  {
    printf("Parent: My parent's process ID: %d \n", getppid());
    printf("Parent: My process ID: %d \n", getpid());
    //printf("Parent: horse: %d \n", horse);
    printf("Parent ptr: %p and its value: %d \n", ptr, *ptr);
    //horse = 1;
    *ptr = 1;
    printf("I am the parent, ptr: %p and its value: %d \n", ptr, *ptr);

    //printf("I am parent and new horse is: %d \n", horse);
    printf("Parent: My child's process ID: %d \n", f);
    //wait(NULL);
    printf("Parent: Terminating...\n");
    exit(0);
  }
  return (0);
}

